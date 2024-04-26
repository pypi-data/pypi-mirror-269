import os
from typing import Union

base_path = os.path.join(os.sep, "bira-iasb", "data", "GROUNDBASED", "BRAMS")


def extract_file(tarpath: str, filename: str) -> Union[bytes, False]:

    import tarfile

    try:

        with tarfile.open(tarpath, "r") as tar:

            for member in tar.getmembers():

                if member.name == filename:

                    with tar.extractfile(member) as extracted_file:

                        return extracted_file.read()
            
            return False

    except (tarfile.ReadError, FileNotFoundError):

        return False


def get(system_code: str, year: int, month: int, day: int, hours: int, minutes: int):

    tar_name = f"RAD_BEDOUR_{str(year).zfill(4)}{str(month).zfill(2)}{str(day).zfill(2)}_{str(hours).zfill(2)}00_{system_code}.tar"
    tar_path = os.path.join(base_path, str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), tar_name)
    wav_name = f"RAD_BEDOUR_{str(year).zfill(4)}{str(month).zfill(2)}{str(day).zfill(2)}_{str(hours).zfill(2)}{str(minutes).zfill(2)}_{system_code}.wav"

    return extract_file(tar_path, wav_name)

