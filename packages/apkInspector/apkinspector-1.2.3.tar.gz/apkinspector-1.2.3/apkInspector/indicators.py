import io

from .extract import extract_file_based_on_header_info
from .headers import ZipEntry
from .axml import ResChunkHeader, StringPoolType, process_elements, XmlResourceMapType, XmlStartElement


def count_eocd(apk_file):
    """
    Counter for the number of time the end of central directory record was found.

    :param apk_file: The APK file e.g. with open('test.apk', 'rb') as apk_file
    :type apk_file: bytesIO
    :return: The count of how many times the end of central directory record was found
    :rtype: int
    """
    apk_file.seek(0)
    content = apk_file.read()
    return content.count(b'\x50\x4b\x05\x06')


def zip_tampering_indicators(apk_file, strict: bool):
    """
    Method to check the for indicators of tampering in the ZIP structure of the APK. These tamperings in the ZIP
    structure, serve as a method of evasion against static analysis tools.

    :param apk_file: The APK file e.g. with open('test.apk', 'rb') as apk_file
    :type apk_file: bytesIO
    :param strict: Whether to be checking strictly or not. Utilizing the application set that was used also for the tests here https://github.com/erev0s/apkInspector/tree/main/tests/top_apps, we tested what kind of indicators would be returned. It turns out that in some cases the local header and the central directory entry for the same file do not have the same values for some keys. So the strict checking was added, to be able to exclude these rare but possible occasions.
    :type strict: bool
    :return: Returns a dictionary with the detected indicators.
    :rtype: dict
    """
    zip_tampering_indicators_dict = {}
    if strict:
        # This is added as strict as a few legitimate APKs do have it for some reason
        count = count_eocd(apk_file)
        if count > 1:
            zip_tampering_indicators_dict['eocd_count'] = count
    zipentry_dict = ZipEntry.parse(apk_file).to_dict()

    unique_keys = list(zipentry_dict["central_directory"].keys() ^ zipentry_dict["local_headers"].keys())
    common_keys = list(set(zipentry_dict["central_directory"].keys()) & set(zipentry_dict["local_headers"].keys()))
    if unique_keys:
        zip_tampering_indicators_dict['unique_entries'] = unique_keys
    for key in common_keys:
        cd_entry = zipentry_dict["central_directory"][key]
        lh_entry = zipentry_dict["local_headers"][key]
        temp = {}
        if cd_entry['compression_method'] not in [0, 8]:
            temp['central compression method'] = cd_entry['compression_method']
        if lh_entry['compression_method'] not in [0, 8]:
            temp['local compression method'] = lh_entry['compression_method']
        if cd_entry['compression_method'] not in [0, 8] or lh_entry['compression_method'] not in [0, 8]:
            indicator = \
                extract_file_based_on_header_info(apk_file, lh_entry, cd_entry)[
                    1]
            temp['actual compression method'] = indicator
        df_keys = local_and_central_header_discrepancies(cd_entry, lh_entry, strict)
        if df_keys:
            temp['differing headers'] = df_keys
        if not temp:
            continue
        zip_tampering_indicators_dict[key] = temp
    return zip_tampering_indicators_dict


def local_and_central_header_discrepancies(dict1, dict2, strict: bool):
    """
    Checking discrepancies between local header values and central directory values

    :param dict1: the central directory dictionary
    :type dict1: dict
    :param dict2: the local headers dictionary
    :type dict2: dict
    :param strict: Boolean for strict checking the headers or not
    :type strict: bool
    :return: Returns a list with the common keys between the dictionaries that have different values.
    :rtype: list
    """
    common_keys = set(dict1.keys()) & set(dict2.keys())
    differences = {key: (dict1[key], dict2[key]) for key in common_keys if dict1[key] != dict2[key]}
    # Display the keys with differing values
    keys = []
    for key, values in dict(sorted(differences.items())).items():
        # strict checking or not: excluding these as they differ often
        if not strict and key in ['extra_field', 'extra_field_length', 'crc32_of_uncompressed_data', 'compressed_size', 'uncompressed_size']:
            continue
        keys.append(key)
    return keys


def manifest_tampering_indicators(manifest):
    """
    Method to check for indicators of tampering in the AndroidManifest.xml

    :param manifest: The AndroidManifest file to check
    :type manifest: bytesIO
    :return: Returns a dictionary with the indicators of tampering for the AndroidManifest
    :rtype: dict
    """
    chunkHeader = ResChunkHeader.parse(manifest)
    manifest_tampering_indicators_dict = {}
    if chunkHeader.type != 3:
        manifest_tampering_indicators_dict['file_type'] = chunkHeader.type
    string_pool = StringPoolType.parse(manifest)
    if len(string_pool.string_offsets) != string_pool.header.string_count:
        manifest_tampering_indicators_dict['string_pool'] = {'string count': string_pool.header.string_count,
                                                             'real string count': len(string_pool.string_offsets)}
    XmlResourceMapType.parse(manifest)
    elements, dummy = process_elements(manifest)
    for element in elements:
        if isinstance(element, XmlStartElement):
            for attr in element.attributes:
                if element.attrext[3] != 20:
                    manifest_tampering_indicators_dict['dummy data between attributes'] = 'found'
                if 0 <= attr.name_index < len(string_pool.strdata):
                    if string_pool.strdata[attr.name_index] == "":
                        manifest_tampering_indicators_dict['dummy attributes'] = 'found (verify manually)'
    if dummy[0]:
        manifest_tampering_indicators_dict['dummy_data_between_elements'] = 'found'
    if dummy[1]:
        manifest_tampering_indicators_dict['wrong_end_namespace_size'] = 'found'
    return manifest_tampering_indicators_dict


def apk_tampering_check(apk_file, strict: bool):
    """
    Method to combine the check for tampering in the zip structure and in the AndroidManifest and return the results.

    :param apk_file: The apk file to check
    :type apk_file: bytesIO
    :param strict: A boolean to strictly check all fields or not. Suggested value: False
    :type strict: bool
    :return: Returns a combined dictionary with the results from the zip_tampering_indicators and the manifest_tampering_indicators
    :rtype: dict
    """
    zip_tampering_indicators_dict = zip_tampering_indicators(apk_file, strict)
    zipentry = ZipEntry.parse(apk_file)
    cd_h_of_file = zipentry.get_central_directory_entry_dict("AndroidManifest.xml")
    local_header_of_file = zipentry.get_local_header_dict("AndroidManifest.xml")
    manifest = io.BytesIO(extract_file_based_on_header_info(apk_file, local_header_of_file, cd_h_of_file)[0])
    manifest_tampering_indicators_dict = manifest_tampering_indicators(manifest)
    return {'zip tampering': zip_tampering_indicators_dict, 'manifest tampering': manifest_tampering_indicators_dict}