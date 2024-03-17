import pkg_resources

# Get a list of all installed packages and their versions
installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

# Print the versions
print("Versions of used modules:")
for package, version in installed_packages.items():
    print(f"{package}: {version}")
