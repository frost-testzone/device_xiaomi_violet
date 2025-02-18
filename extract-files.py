#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

blob_fixups: blob_fixups_user_type = {
    ('vendor/lib/libwvhidl.so', 'vendor/lib/mediadrm/libwvdrmengine.so', 'vendor/lib64/libwvhidl.so', 'vendor/lib64/mediadrm/libwvdrmengine.so'): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v34.so'),
    ('vendor/lib/mediadrm/libwvdrmengine.so', 'vendor/lib64/libwvhidl.so', 'vendor/lib64/mediadrm/libwvdrmengine.so'): blob_fixup()
        .replace_needed('libprotobuf-cpp-lite-3.9.1.so', 'libprotobuf-cpp-full-3.9.1.so'),
    ('vendor/lib64/libvidhance.so', 'vendor/lib64/camera/components/com.vidhance.node.eis.so'): blob_fixup()
        .add_needed('libc++demangle.so')
        .add_needed('libcomparetf2_shim.so'),
    'vendor/lib64/camera/components/com.vidhance.stats.aec_dmbr.so': blob_fixup()
        .add_needed('libcomparetf2_shim.so'),
    'vendor/lib64/hw/camera.qcom.so': blob_fixup()
        .binary_regex_replace(b'libc\+\+.so', b'libc29.so'),
    ('vendor/bin/mlipayd@1.1', 'vendor/lib64/libmlipay.so', 'vendor/lib64/libmlipay@1.1.so'): blob_fixup()
        .remove_needed('vendor.xiaomi.hardware.mtdservice@1.0.so'),
    ('system_ext/lib64/libwfdnative.so', 'system_ext/lib/libwfdnative.so', 'vendor/lib64/libgoodixhwfingerprint.so'): blob_fixup()
        .remove_needed('android.hidl.base@1.0.so'),
    'vendor/etc/camera/camxoverridesettings.txt': blob_fixup()
        .regex_replace('0x10080', '0')
        .regex_replace('0x1F', '0'),
    'vendor/lib64/libvendor.goodix.hardware.interfaces.biometrics.fingerprint@2.1.so': blob_fixup()
        .remove_needed('libhidlbase.so')
        .binary_regex_replace(b'libhidltransport.so', b'libhidlbase-v32.so\x00'),
}  # fmt: skip

module = ExtractUtilsModule(
    'violet',
    'xiaomi',
    blob_fixups=blob_fixups,
    check_elf=False,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
