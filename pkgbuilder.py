#!/usr/bin/env python3
import urllib.request
import hashlib
import yaml

def read_yaml_file(yaml_file_path: str) -> dict:
  with open(yaml_file_path, mode="r", encoding="utf-8") as file:
    return yaml.load(file, yaml.SafeLoader)

def write_yaml_file(yaml_file_path: str, obj):
  with open(yaml_file_path, mode="w", encoding="utf-8") as file:
    yaml.dump(obj, file)

class Pkgbuilder:
    def __init__(self, config: dict):
        self.config = config

    def print(self):
        for person in self.config["people"]:
            self.print_person(person)
        self.print_header()
        self.print_sources()
        self.print_build()
        self.print_package()
        self.print_options()

    def print_options(self):
        opts = []
        for (k,v) in self.config["options"].items():
            if v:
                opts.append(k)
            else:
                opts.append("!" + k)
        print("options=(%s)" % " ".join(opts))

    def print_person(self, person: dict):
        print("# %s: %s %s <%s>" % (
            person["role"], person["surname"], person["name"], person["email"]
        ))

    def print_header(self):
        print("pkgname=%s" % self.config["pkgname"])
        print("pkgver=%s" % self.config["pkgver"])
        print("pkgrel=%s" % self.config["pkgrel"])
        print("pkgdesc=\'%s\'" % self.config["pkgdesc"])
        print("license=('%s')" % self.config["license"])
        print("arch=(%s)" % " ".join(["'%s'" % arch for arch in self.config["arch"]]))
        print("makedepends=(%s)" % " ".join(["'%s'" % makedepends for makedepends in self.config["makedepends"]]))
        print("url='%s'" % self.config["url"])

    def print_sources(self):
        print("_archive='%s'" % self.config["archive"])
        print("source=(\"$pkgname-$pkgver.tar.gz::$_archive/$pkgver.tar.gz\")")
        print("sha256sums=('%s')" % self.compute_hash())

    def compute_hash(self):
        link = "%s/%s.tar.gz" % (self.config["archive"], self.config["pkgver"])
        file = "%s.tar.gz" % self.config["pkgver"]
        urllib.request.urlretrieve(link, file)
        hash = b""
        with open(file, mode="rb") as _in:
            hash = hashlib.sha256(_in.read()).digest()
        return hash.hex()

    def print_build(self):
        print("build() {")
        print("  cd %s" % "$pkgname-$pkgver")
        for line in self.config["build"]:
            print("  " + line)
        print("}")

    def print_package(self):
        print("package() {")
        print("  cd %s" % "$pkgname-$pkgver")
        for line in self.config["package"]:
            print("  " + line)
        print("}")

if __name__ == "__main__":
    config = read_yaml_file('pkgbuild.yaml')
    Pkgbuilder(config).print()
