from __future__ import annotations

import json
import os

from licensespring.licensefile.config import Configuration
from licensespring.licensefile.default_crypto import DefaultCryptoProvider
from licensespring.licensefile.error import ErrorType, LicenseDeleted
from licensespring.licensefile.license_data import LicenseData


class DataStorage(DefaultCryptoProvider):
    """
    Extends DefaultCryptoProvider to handle license file cache operations, including saving to and loading from a .key file.

    Attributes:
        _conf (Configuration): Configuration object containing settings and parameters.
        _cache (LicenseData): Instance of LicenseData for managing license attributes in memory.
        _filename (str): The name of the file used for storing the license information.
        _license_path (str): The file path where the license file is stored.

    Methods:
        cache: Returns the current license data stored in memory.
        license_path: Returns the file path for the license file.
        save_licensefile(): Encrypts and saves the license data to a file.
        load_licensefile(): Loads and decrypts the license data from a file.
        set_path(product_code, custom_path): Sets the file path for the license file based on the operating system.
        delete_licensefile(): Deletes the license file and clears the license data in memory.
    """

    def __init__(self, conf: Configuration):
        self._conf = conf
        super().__init__(self._conf._file_key, self._conf._file_iv)

        self._cache = LicenseData(
            product=self._conf._product,
            hardwareID=self._conf._hardware_id_provider.get_id(self),
            grace_period_conf=self._conf.grace_period_conf,
        )

        self._filename = self._conf._filename
        self._license_path = self.set_path(self._conf._product, self._conf._file_path)

    @property
    def cache(self):
        return self._cache.to_json()

    @property
    def license_path(self):
        return self._license_path

    def save_licensefile(self):
        """
        Creates path for licensefile
        Saves encrypted string of licensefile JSON
        """
        json_string_encrypted = self.encrypt(self._cache.to_json())
        with self._cache._lock:
            # Create the folder if it does not exist
            if not os.path.exists(self.license_path):
                os.makedirs(self.license_path)

            with open(
                os.path.join(self.license_path, self._filename + ".key"), "w"
            ) as file:
                file.write(json_string_encrypted)

    def load_licensefile(self) -> dict:
        """
        Loads and decrypts licensefile

        Returns:
            dict: licensefile
        """

        try:
            with open(
                os.path.join(self.license_path, self._filename + ".key"), "r"
            ) as file:
                json_string_encrypted = file.read()

            licensefile_dict = json.loads(self.decrypt(json_string_encrypted))

            self._cache.from_json_to_attr(licensefile_dict)

            self._cache.grace_period_conf = self._conf.grace_period_conf

            return licensefile_dict
        except FileNotFoundError:
            raise LicenseDeleted(ErrorType.NO_LICENSEFILE, "Licensefile doesn't exist")

    def set_path(self, product_code: str, custom_path=None) -> str:
        """
        Set path for licensefile

        Parameters:
            product_code (str): short product code of LicenseSpring product
            custom_path(str,optional): custom path of licensefile

        Returns:
            str: Path of licensefile
        """

        if custom_path is not None:
            return custom_path

        if os.name == "nt":  # Windows
            base_path = os.path.join(
                os.environ.get("SystemDrive"), "Users", os.environ.get("USERNAME")
            )
            return os.path.join(
                base_path, "AppData", "Local", "LicenseSpring", product_code
            )

        elif os.name == "posix":  # Linux and macOS
            if "HOME" in os.environ:
                base_path = os.environ["HOME"]
                return os.path.join(
                    base_path, ".LicenseSpring", "LicenseSpring", product_code
                )

            else:  # macOS and other POSIX systems
                base_path = os.path.expanduser("~")
                return os.path.join(
                    base_path,
                    "Library",
                    "Application Support",
                    "LicenseSpring",
                    product_code,
                )

        else:
            raise Exception("Unsupported operating system")

    def delete_licensefile(self):
        """
        Permanently deletes licensefile and clears cache

        Returns: None
        """

        if os.path.exists(os.path.join(self.license_path)):
            os.remove(os.path.join(self.license_path, self._filename + ".key"))

        self._cache = LicenseData(
            product=self._conf._product,
            hardwareID=self._conf._hardware_id_provider.get_id(self),
            grace_period_conf=self._conf.grace_period_conf,
        )
