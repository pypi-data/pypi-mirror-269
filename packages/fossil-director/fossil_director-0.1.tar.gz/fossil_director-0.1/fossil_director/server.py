import subprocess
import os.path
from socketserver import ThreadingTCPServer, StreamRequestHandler


class FossilProxyHandler(StreamRequestHandler):
    def parse_scgi(self):
        buf = self.request.recv(8192)
        header_length = int(buf[: buf.index(b":")])
        size = []
        i = buf.index(b"CONTENT_LENGTH\x00") + 15
        while 1:
            next_chr = buf[i]
            if next_chr == 0:
                break
            size.append(next_chr)
            i += 1
        if size:
            size = int(bytes(size))
        else:
            size = 0

        i = buf.index(b"HTTP_HOST\x00") + 10
        next_chr = buf[i]
        hostname = []

        while next_chr:
            hostname.append(next_chr)
            i += 1
            next_chr = buf[i]

        hostname = bytes(hostname).decode().split(":")[0]
        if size:
            wanted = (size + header_length) - len(buf)
            while wanted > 0:
                chunk = self.request.recv(8192)
                if not chunk:
                    break
                buf += chunk
                wanted -= len(chunk)
        return buf, hostname

    def parse_http(self):
        buf = b""
        doing_headers = True
        hostname = None
        content_length = 0
        while True:
            line = self.rfile.readline()
            buf += line
            if line in (b"", b"\r\n"):
                break

            if hostname is None and line.startswith(b"Host: "):
                hostname = line.split(b" ", 1)[1].strip().decode().split(":")[0]

            elif line.startswith(b"Content-Length: "):
                content_length = int(line.split(b" ", 1)[1].strip())
        if content_length:
            buf += self.rfile.read(content_length)

    def handle(self):
        if self.server.is_scgi:
            buf, hostname = self.parse_scgi()
        else:
            buf, hostname = self.parse_http()

        command = self.server.get_repo(hostname)
        if command:
            self.run_fossil(command, buf)
        else:
            self.wfile.write(b"400 Bad Request\r\n\r\n")
        self.wfile.close()

    def run_fossil(self, command, buf):
        output = subprocess.run(command, input=buf, capture_output=True)
        self.wfile.write(output.stdout)


class FossilProxyServer(ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, config_file):
        self.config, self.repos, self.is_scgi = self.configure(config_file)
        super().__init__(
            (self.config.get("server", "host"), self.config.getint("server", "port")),
            FossilProxyHandler,
        )

    def configure(self, config_file: str):
        from configparser import ConfigParser

        config = ConfigParser()
        config.read_dict(
            {
                "server": {
                    "host": "127.0.0.1",
                    "port": 7000,
                    "fossil_cmd": "/usr/local/bin/fossil",
                    "scgi": False,
                }
            }
        )
        config.read(config_file)
        repos = {}
        is_scgi = config.getboolean("server", "scgi")

        for section in config.sections():
            if section != "server":
                args = [config.get("server", "fossil_cmd"), "http"]
                if is_scgi:
                    args.append("--scgi")
                base_url = config.get(section, "baseurl", fallback="")
                if base_url:
                    args.extend(["--baseurl", base_url])
                repolist = config.getboolean(section, "repolist", fallback=False)
                if repolist:
                    args.append("--repolist")
                extra_args = config.get(section, "args", fallback="")
                if extra_args:
                    args.extend(extra_args.split(","))
                args.append(os.path.abspath(config.get(section, "repo")))
                repos[section.lower()] = args

        print(f"Using fossil: {config.get('server', 'fossil_cmd'):>60s}")
        print("Domains:")
        for host, info in repos.items():
            print(f"{host:<20s}{info[-1]:>60s}")
        return config, repos, is_scgi

    def get_repo(self, hostname):
        return self.repos.get(hostname, None) or self.repos.get("DEFAULT", None)


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: fossil-director [CONFIG FILE]")
        sys.exit(-1)
    config_file = sys.argv[1]
    if not os.path.exists(config_file):
        print(f"{config_file} does not exist")
        sys.exit(-1)
    with FossilProxyServer(config_file) as server:
        server_type = "SCGI" if server.is_scgi else "HTTP"
        print("=" * 40)
        print(
            f"Running {server_type} on {server.server_address[0]}:{server.server_address[1]}"
        )
        print("=" * 40)
        server.serve_forever()


if __name__ == "__main__":
    main()
