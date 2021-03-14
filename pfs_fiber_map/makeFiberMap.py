#!/usr/bin/env python

import os
import numpy as np
# from scipy import ndimage
# from scipy.optimize import curve_fit

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)


def get_mtp_group(fh, sp):
    """
    query MTP group and associating cobra field
    Parameters
    ----------
    fh: `int`
        fiber hole
    sp: `int`
        spectrograph module number

    Returns
    -------
    mtp: `str`
        mtp group
    mf: `int`
        the module number per field sections
    fld : `int`
        field number on PFI
    """
    # U3 groups: 29 fibers each
    if 2 <= fh < 31:
        mtp = "U3-1"
    elif 31 <= fh < 62:
        mtp = "U3-2"
    elif 62 <= fh < 91:
        mtp = "U3-3"
    # U2 groups: 29 fibers each
    elif 94 <= fh < 123:
        mtp = "U2-1"
    elif 123 <= fh < 154:
        mtp = "U2-2"
    elif 154 <= fh < 183:
        mtp = "U2-3"
    # U1 groups: 28 fibers each
    elif 186 <= fh < 214:
        mtp = "U1-1"
    elif 214 <= fh < 244:
        mtp = "U1-2"
    elif 244 <= fh < 272:
        mtp = "U1-3"
    # D0 groups: 29 fibers each
    elif 274 <= fh < 303:
        mtp = "D0-1"
    elif 303 <= fh < 353:
        mtp = "D0-2"
    elif 353 <= fh < 382:
        mtp = "D0-3"
    # D1 groups: 28 fibers each
    elif 384 <= fh < 412:
        mtp = "D1-1"
    elif 412 <= fh < 442:
        mtp = "D1-2"
    elif 442 <= fh < 470:
        mtp = "D1-3"
    # D2 groups: 28 fibers each
    elif 473 <= fh < 501:
        mtp = "D2-1"
    elif 501 <= fh < 531:
        mtp = "D2-2"
    elif 531 <= fh < 559:
        mtp = "D2-3"
    # D3 groups: 29 fibers each
    elif 562 <= fh < 591:
        mtp = "D3-1"
    elif 591 <= fh < 622:
        mtp = "D3-2"
    elif 622 <= fh < 651:
        mtp = "D3-3"
    else:
        logging.warning("Fiber does not seem to science fiber..?")

    # The number of the science fibers for each group
    if mtp[0:2] in ['U3', 'U2', 'D3', 'D0']:
        max_fib = 29
    elif mtp[0:2] in ['U1', 'D1', 'D2']:
        max_fib = 28
    else:
        logging.warning("MTP group looks strange...")

    if mtp.startswith('U3') or mtp.startswith('U1'):
        mf_i = 1
    elif mtp.startswith('D3') or mtp.startswith('D2'):
        mf_i = 2
    elif mtp.startswith('U2') or mtp.startswith('D1'):
        mf_i = 3
    elif mtp.startswith('D0'):
        mf_i = 4
    else:
        logging.warning("MTP group looks strange...")

    # pfi field labelled with color
    # red and green fields have 29 cobras, while blue and yellow fields 28
    # in design
    pfi_to_sps = {1: 'red', 2: 'green', 3: 'blue', 4: 'yellow'}

    mf = (mf_i - 1)*4 + sp

    emp_flag = 0
    if mtp.startswith('D0') and pfi_to_sps[sp] == 'blue':
        mf = 13
        emp_flag = 1
    if mtp.startswith('D0') and pfi_to_sps[sp] == 'yellow':
        mf = 14
        emp_flag = 1

    fld = int(mtp[-1])

    return mtp, mf, fld, max_fib, emp_flag


def get_mtp_hole(cnt, max_fib, emp_flag):

    used_hole = list(range(2, 32))
    used_hole.remove(25)

    if max_fib == 28:
        used_hole.remove(8)

    hole_a = used_hole[cnt-1]

    return hole_a


def flip_mtp_hole(hole):

    row = np.floor((hole-1)/8.)+1
    col = (hole-1)%8
    hole_flip = int((row-1)*8 + (8-col))

    return hole_flip


def invert_mtp_hole(hole):

    hole_invt = 33 - hole

    return hole_invt


def calc_cob_position(pid, mf, fld, m):

    # fundermental spacing of cobra
    Dely = 8./2.
    Delx = 8.*np.sqrt(3.)/2

    x1 = -1.*Delx*((pid - 1)%2 + 2*mf - 1)
    y1 = -1.*Dely*(pid - 2*mf)

    if fld == 1:
        x = x1
        y = y1
    else:
        x = x1*np.cos(2*np.pi*(fld-1)/3) + y1*np.sin(2*np.pi*(fld-1)/3)
        y = -x1*np.sin(2*np.pi*(fld-1)/3) + y1*np.cos(2*np.pi*(fld-1)/3)

    r = np.sqrt(x*x+y*y)

    return x, y, r


def add_sunss(idc, sunss_dict):

    fibid = idc
    fibid = fibid[:5] + 'X' + fibid[6:]   # replace sp to X
    fibid = fibid.rsplit('-', 1)[0]  # trim cobra pid
    if fibid in sunss_dict:
        logging.debug("SuNSS")
        sunss_id = sunss_dict[fibid]
    else:
        sunss_id = 'emp'

    return sunss_id


def make_grand_map():

    # Each spectrograrh have 651 fiber holes
    # Engineering fibers
    fh_eng = [1, 45, 92, 137, 184, 229, 273, 316, 336,
              382, 426, 471, 515, 560, 607, 651]
    # Blank fibers
    fh_emp = [44, 91, 93, 136, 183, 185, 228, 272] + \
             list(range(317, 336)) + \
             [383, 427, 470, 472, 516, 559, 561, 608]

    # the number of science fibers per SpS
    # in design
    sfib_max = [600, 600, 597, 597]

    # load sunss mapping
    sunss_ids, sunss_fib = np.loadtxt('SunssFiberMap_v2.10_edit.txt', dtype='str', unpack=True)
    sunss_dict = dict(zip(sunss_fib, sunss_ids))
    logging.debug(sunss_dict)

    header = ('\\cob fld cf mf  cm mod'
              '      x        y       r   sp  fh  sfib  sunss'
              '   id(A)        id(C)        id(BA)       id(BC)')
    print(header)

    for sp in range(1, 5):  # SM1 -- SM4
        cnt = 1
        sfib_start = 0 + int(np.sum(sfib_max[0:sp-1]))
        sfib_sp = 1
        emp_flag = 0
        for fh in range(1, 652):  # fh is 1--651
            if fh in fh_eng:  # Engineering fibers
                pass
            elif fh in fh_emp:  # Blank fibers
                pass
            else:  # Science fibers
                # print(cnt)

                mtp, mf, fld, max_fib, emp_flag = get_mtp_group(fh, sp)

                m = mf + (fld-1)*14
                if max_fib == 28:
                    pid = cnt + 29  # cm in Jim's doc
                    mod = f'{m}B'
                elif max_fib == 29 and emp_flag == 1:
                    if cnt < 7:
                        pid = cnt + 29
                    elif cnt == 7:
                        logging.info("No Cobra here")
                        logging.info(fh)
                        emp_flag = 0
                        cnt += 1
                        continue
                    else:
                        pid = (cnt-1) + 29
                    mod = f'{m}B'
                else:
                    pid = cnt  # cm in Jim's doc
                    mod = f'{m}A'

                m = 1 if pid % 2 == 0 else 0

                cf = pid + 57*(mf - 1)
                cob = cf + 798*(fld-1)
                x, y, r = calc_cob_position(pid, mf, fld, m)

                hole_a = get_mtp_hole(cnt, max_fib, emp_flag)
                hole_c = flip_mtp_hole(hole_a)
                hole_bc = invert_mtp_hole(hole_a)
                hole_ba = invert_mtp_hole(hole_c)

                # fiber ID on MTP A side
                ida = f'{mtp}-{sp}-{hole_a}-{pid}'
                # fiber ID on MTP C side
                idc = f'{mtp}-{sp}-{hole_c}-{pid}'
                # fiber ID on MTP BA side
                idba = f'{mtp}-{sp}-{hole_ba}-{pid}'
                # fiber ID on MTP BC side
                idbc = f'{mtp}-{sp}-{hole_bc}-{pid}'
                sfib = sfib_sp + sfib_start

                # get sunss id
                sunss_id = add_sunss(idc, sunss_dict)

                str = (f'{cob:>4}  {fld} {cf:>3} {mf:>2}  {pid:>2} {mod:>3} '
                       f'{x:8.3f} {y:8.3f} {r:7.3f}  {sp} {fh:>3}  {sfib:>4} '
                       f'{sunss_id:>4}  '
                       f'{ida:<12} {idc:<12} {idba:<12} {idbc:<12}')

                print(str)

                sfib_sp += 1
                cnt += 1
                emp_flag = 0
                if cnt > max_fib:
                    cnt = 1


if __name__ == '__main__':

    make_grand_map()
