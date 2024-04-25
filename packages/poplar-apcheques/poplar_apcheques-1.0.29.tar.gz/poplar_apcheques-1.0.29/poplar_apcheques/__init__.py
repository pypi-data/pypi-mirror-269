try:
    from accpac import *
except ImportError as e:
    pass

import io
from pathlib import Path
from datetime import datetime

from reportlab.pdfgen import canvas
from pdfrw import PdfReader, PdfWriter, PageMerge

from reportlab.lib.utils import ImageReader

from extools.view import exview
from extools.view.errors import ExViewError, ExViewRecordDoesNotExist
from excrypto.gnupg import GnuPGPublicKeyEncryptor, GnuPGKeyManager

def signatures_path():
    try:
        with exview("PPAPCHQ.PPAPCHQ", fetch=True) as exv:
            sigroot = exv.get("SIGROOT")
            if sigroot:
                return Path(sigroot)
    except ExViewRecordDoesNotExist:
        pass
    return Path(getOrgPath(), '.signatures')

def working_path():
    try:
        with exview("PPAPCHQ.PPAPCHQ", fetch=True) as exv:
            workroot = exv.get("WORKROOT")
            if workroot:
                return Path(workroot)
    except ExViewRecordDoesNotExist:
        pass
    return Path(getOrgPath(), '.cheque_reports')

def gnupg_home():
    return Path(getOrgPath(), '.gnupg', user)

def gnupg_system_home():
    return Path(getOrgPath(), '.gnupg', org)

def gnupg_system_passphrase():
    return "{}-passphrase".format(org.lower())

def gnupg_system_user():
    return "system"

def gnupg_system_email():
    return "{}@{}".format(gnupg_system_user(), org.lower())

def gnupg_system_fingerprint():
    if not gnupg_system_home().exists():
        gnupg_system_home().mkdir(parents=True)
    key_manager = GnuPGKeyManager(user, gnupg_system_home())
    key = key_manager.first_key()

    if not (key and key.get("fingerprint")):
        key = key_manager.generate_key(
                gnupg_system_passphrase(),
                gnupg_system_user(),
                gnupg_system_email())
        fingerprint = key.fingerprint
    else:
        fingerprint = key.get("fingerprint")

    return fingerprint

def gnupg_system_file_bytes(input_file):
    data = bytes()
    if input_file.suffix == ".gpg":
        # System decrypt to Bytes IO
        fingerprint = gnupg_system_fingerprint()
        encryptor = GnuPGPublicKeyEncryptor(
                gnupg_system_home(), fingerprint, gnupg_system_passphrase())
        data = encryptor.decrypt_file(input_file)
    else:
        with input_file.open('rb') as f:
            data = f.read()

    return data

def gnupg_system_encrypt_bytes(input):
    fingerprint = gnupg_system_fingerprint()
    encryptor = GnuPGPublicKeyEncryptor(
            gnupg_system_home(), fingerprint, gnupg_system_passphrase())
    return encryptor.encrypt_stream(input, [gnupg_system_email(), ])

def get_print_destination():
    try:
        with exview("PPAPCHQ.PPAPCHQ") as config:
            config.recordClear()
            config.browse("", 1)
            config.fetch()
            return config.get("DEST")
    except ExViewError as err:
        pass
    return None

def cheque_stock_for_batch(batchno):
    # find the check stock code.
    try:
        with exview("AP0030", seek_to={
                "PAYMTYPE": "PY", "CNTBTCH": batchno}) as apbta:
            with exview("BK0008") as bkform:
                bkform.browse('BANK = "{}"'.format(apbta.idbank), 1)
                bkform.fetch()
                return bkform.formid
    except ExViewError as e:
        pass
    return ""

def merge_pdf_bytes(base, overlay):
    output = io.BytesIO()
    try:
        base.seek(0)
        overlay.seek(0)
        # define the reader and writer objects
        reader_input = PdfReader(base)
        watermark_input = PdfReader(overlay)
        watermark = watermark_input.pages[0]

        # go through the pages one after the next
        for current_page in range(len(reader_input.pages)):
            merger = PageMerge(reader_input.pages[current_page])
            merger.add(watermark).render()

        # write the modified content to disk
        writer_output = PdfWriter()
        writer_output.write(output, reader_input)
    except Exception as err:
        pass

    return output

def prompt_for_passphrase():
    passphrase = ''
    ppath = Path(signatures_path(),
                 datetime.now().strftime("%Y%m%d%H%M%S"))

    if not ppath.parent.exists():
        ppath.parent.mkdir(parents=True)

    try:
        # Prompt for pasphrase
        params = "KEY1={}\n".format(str(ppath))
        openExtenderUI("PPAPCHQ.PassphraseUI.py", params, True)
        with ppath.open('r') as f:
            passphrase = f.read()
    finally:
        if ppath.exists():
            ppath.unlink()

    return passphrase

class OverlayCreateError(RuntimeError):
    pass

def overlay_for_stock(stockcode, user):
    try:
        with exview("PPAPCHQ.PPAPCHQU", seek_to={"USERID": user}) as exv:
            sigpath = Path(signatures_path(), exv.sigpath)
            passphrase_protected = exv.pp
            fingerprint = exv.fingerp
    except ExViewError as e:
        errmsg = "No signatures configured for user {}".format(stockcode, user)
        raise OverlayCreateError(errmsg)

    try:
        with exview("PPAPCHQ.PPAPCHQS", seek_to={
                "FORMID": stockcode, "USERID": user}) as exv:
            top = exv.top
            left = exv.left
            width = exv.width
            height = exv.height
    except ExViewError as e:
        errmsg = "No check stock configured for {} {}".format(stockcode, user)
        raise OverlayCreateError(errmsg)

    max_tries = 3
    tries = 1
    while True:
        try:
            passphrase = None
            if passphrase_protected:
                passphrase = prompt_for_passphrase()
                if not passphrase:
                    raise OverlayCreateError(
                            "Signature encrypted with passphrase but none provided.")

            encryptor = GnuPGPublicKeyEncryptor(gnupg_home(), fingerprint, passphrase)

            data = encryptor.decrypt_file(sigpath)
            if not data:
                errmsg = "decryption result empty. check extools log."
                raise OverlayCreateError(errmsg)
            else:
                break
        except OverlayCreateError as e:
            if tries <= max_tries:
                tries += 1
            else:
                raise OverlayCreateError("too many failed password attempts.")

    overlay = io.BytesIO()

    if data:
        try:
            png = ImageReader(io.BytesIO(data))
            c = canvas.Canvas(overlay)
            c.drawImage(png, left, top, width, height)
            c.save()
        except Exception as err:
            errmsg = "creating signature overlay failed: {}".format(err)
            raise OverlayCreateError(errmsg)

    return overlay
