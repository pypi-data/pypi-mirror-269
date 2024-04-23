import os.path
from peegy.processing.tools.filters.resampling import eeg_resampling
from peegy.processing.events.event_tools import get_event_times, events_to_samples_array
import os
import numpy as np
import logging
import astropy.units as u
from tqdm import tqdm
import mmap
import datetime
from peegy.processing.events import event_tools
from peegy.io.eeg.reader import eeg_reader
from pathlib import Path
import shutil
log = logging.getLogger()


def data_to_bdf(data: np.array = None,
                events: np.array = None,
                output_file_name: str = None,
                header: dict = None,
                fs: u.Quantity = None):

    n_records = np.ceil((data.shape[0] / fs.to('Hz')).value /
                        header['duration_data_record'].to('s').value).astype(int)
    n_samples_record = np.round(fs.to('Hz').value * header['duration_data_record'].to('s').value).astype(int)

    with open(output_file_name, 'wb') as f:
        # write header (256 bytes)
        f.write(np.uint8(header['identification_code']))
        f.write('{:<7}'.format(header['version'])[0:7].encode('ascii'))
        f.write('{:<80}'.format(header['subject_id'])[0:80].encode('ascii'))
        f.write('{:<80}'.format(header['recording_id'])[0:80].encode('ascii'))
        f.write('{:<8}'.format(header['start_date'])[0:8].encode('ascii'))
        f.write('{:<8}'.format(header['start_time'])[0:8].encode('ascii'))
        f.write(str(header['bytes_in_header']).zfill(8).encode('ascii'))
        f.write('{:<44}'.format(header['data_format'])[0:44].encode('ascii'))
        f.write(str(n_records).zfill(8).encode('ascii'))
        f.write(str(int(header['duration_data_record'].value)).zfill(8)[0:8].encode('ascii'))
        f.write(str(header['n_channels']).zfill(4).encode('ascii'))
        [f.write('{:<16}'.format(header['channels'][i].label)[0:16].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<80}'.format(header['transducer'][i])[0:80].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(header['physical_dimension'][i])[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(header['physical_minimum'][i])[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(header['physical_maximum'][i])[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(header['digital_minimum'][i])[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(header['digital_maximum'][i])[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<80}'.format(header['pre_filtering'][i])[0:80].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(n_samples_record)[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<32}'.format(header['reserved'][i])[0:32].encode('ascii')) for i in
         range(header['n_channels'])]
        # all channels need to have the same units
        assert np.unique(header['physical_dimension'][:-1]).size == 1
        data_to_pack = data.to(header['physical_dimension'][0]).value
        data_events = events
        data_to_pack = np.hstack([data_to_pack, data_events])
        data_to_pack = (data_to_pack / header['gain']).astype(np.int32)

        current_data = np.zeros((n_samples_record, data_to_pack.shape[1]), dtype=np.int32)
        for _nr in range(n_records):
            current_data[:] = 0
            _ini = _nr * n_samples_record
            _end = np.minimum((_nr + 1) * n_samples_record, data_to_pack.shape[0])
            _c_record_length = _end - _ini
            current_data[0:_c_record_length, :] = data_to_pack[_ini: _end, :]
            flat_data = current_data.reshape(-1, order='F')
            encoded_array = flat_data.astype(dtype='<i4').tobytes()
            mm = mmap.mmap(-1, len(encoded_array))
            mm.write(encoded_array)
            mm.seek(0)
            for _i in tqdm(range(flat_data.shape[0]),
                           desc='writing record {:} to bdf file {:}'.format(_nr, output_file_name)):
                f.write(mm.read(3))  # write 3 bytes
                mm.read(1)  # skip 4th byte


def clip_bdf(ini_time: u.Quantity = 0 * u.s,
             end_time: u.Quantity = np.inf * u.s,
             input_file_name: str = None,
             output_file_name: str = None,
             ):
    """
    This function generates a new bdf file from a given to an end time.
    :param ini_time: initial time to obtain data
    :param end_time: end time to obtain data
    :param input_file_name: full path of bdf to obtain the data from
    :param output_file_name: full path of the new bdf file
    :return:
    """

    reader = eeg_reader(file_name=input_file_name)
    header = reader._header
    ini_time = np.round(ini_time / header['duration_data_record']) * header['duration_data_record']
    duration = end_time - ini_time
    time_format = r'%H.%M.%S'
    date_format = r'%d.%m.%y'
    date = datetime.datetime.strptime(header['start_date'] + '-' + header['start_time'],
                                      date_format + '-' + time_format)
    new_starting_date = date + datetime.timedelta(seconds=ini_time.value)
    new_date = new_starting_date.strftime(date_format)
    new_time = new_starting_date.strftime(time_format)

    if end_time == np.inf * u.s:
        duration = header['number_records'] * header['duration_data_record'] - ini_time
    n_records = int(duration / header['duration_data_record'])
    start_offset = (3 * ini_time.value * np.sum(header['number_samples_per_record'])).astype(np.int64)
    buffer_size = (3 * duration.value * np.sum(header['number_samples_per_record'])).astype(np.int64)
    # skip first 256 bytes + 256 * N channels
    header_off_set = 256 * (1 + header['n_channels'])

    with open(output_file_name, 'wb') as f:
        # write header (256 bytes plus 256 * n_channels)
        f.write(np.uint8(header['identification_code']))
        f.write('{:<7}'.format(header['version'])[0:7].encode('ascii'))
        f.write('{:<80}'.format(header['subject_id'])[0:80].encode('ascii'))
        f.write('{:<80}'.format(header['recording_id'])[0:80].encode('ascii'))
        f.write('{:<8}'.format(new_date)[0:8].encode('ascii'))
        f.write('{:<8}'.format(new_time)[0:8].encode('ascii'))
        f.write(str(header['bytes_in_header']).zfill(8).encode('ascii'))
        f.write('{:<44}'.format(header['data_format'])[0:44].encode('ascii'))
        f.write(str(n_records).zfill(8).encode('ascii'))
        f.write(str(int(header['duration_data_record'].value)).zfill(8)[0:8].encode('ascii'))
        f.write(str(header['n_channels']).zfill(4).encode('ascii'))
        [f.write('{:<16}'.format(header['channels'][i].label)[0:16].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<80}'.format(header['transducer'][i])[0:80].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(header['physical_dimension'][i])[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(header['physical_minimum'][i])[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(header['physical_maximum'][i])[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(header['digital_minimum'][i])[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(header['digital_maximum'][i])[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<80}'.format(header['pre_filtering'][i])[0:80].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<8}'.format(header['number_samples_per_record'][i])[0:8].encode('ascii')) for i in
         range(header['n_channels'])]
        [f.write('{:<32}'.format(header['reserved'][i])[0:32].encode('ascii')) for i in
         range(header['n_channels'])]
        with open(input_file_name, 'rb') as input_f:
            input_f.seek(header_off_set + start_offset)
            f.write(input_f.read(buffer_size))


def split_bdf_by_event_code(
              input_file_name: str = None,
              output_path: str = None,
              output_file_name: str = None,
              event_code: float = None,
              ini_offset: u.Quantity = 0 * u.s,
              end_offset: u.Quantity = None,
              trash_original: bool = False
              ):
    """
    This function generates several bdf files based on the event code used to split the data.
    :param input_file_name: full path of bdf to obtain the data from
    :param output_path: path to save files
    :param output_file_name: name of output files. The base name and a number will be returned for each output file
    :param event_code: event number to be found to split file
    :param ini_offset: initial time offset from found event. Note that records offsets will be rounded to
     duration_data_record
    :param end_offset: end time offset from found event. Note that records offsets will be rounded to
    duration_data_record
    :param trash_original: if true, the original file will be moved to .trash folder in the same directory
    :return:
    """

    reader = eeg_reader(file_name=input_file_name)
    raw_events = reader.get_events()
    events = event_tools.Events(event_tools.detect_events(event_channel=raw_events, fs=reader.fs))
    events.summary()
    times = events.get_events_time(code=event_code)
    if not times.size:
        print('no events with code {:} were found in file {:}'.format(event_code, reader.file_name))
        return
    duration_data_record = reader._header['duration_data_record']
    if end_offset is None:
        end_offset = -duration_data_record
    if output_file_name is None:
        _, _file_name = os.path.split(input_file_name)
        output_file_name = _file_name
    if output_path is None:
        _path, _ = os.path.split(input_file_name)
        output_path = Path(_path)
    ini_time = [np.floor((_t + ini_offset) / duration_data_record) * duration_data_record for _t in times]
    end_time = [np.floor((_t + end_offset) / duration_data_record) * duration_data_record for _t in times[1:]]
    end_time.append(np.inf * u.s)
    for _i, (_ini_time, _end_time) in tqdm(enumerate(zip(ini_time, end_time)),
                                           desc='splitting file {:}'.format(reader.file_name)):
        Path(output_path).mkdir(parents=True, exist_ok=True)
        _name, _ext = os.path.splitext(output_file_name)
        _output = Path.joinpath(output_path, '{:}_{:}{:}'.format(_name, _i + 1, _ext))
        print('saving {:}'.format(_output))
        clip_bdf(input_file_name=input_file_name,
                 ini_time=_ini_time,
                 end_time=_end_time,
                 output_file_name=_output)

    if trash_original:
        _path, _name = os.path.split(input_file_name)
        _trash_path = Path(_path).joinpath('.trash')
        Path(_trash_path).mkdir(parents=True, exist_ok=True)
        shutil.move(input_file_name, _trash_path.joinpath(_name))
        print('Original file {:} moved to {:}'.format(input_file_name,
                                                      _trash_path.joinpath(_name)))


def change_subject_id(file_name: str = None,
                      subject_id: str = ''):
    """
    This function will change the subject_id in a .bdf or .edf file. Useful to anonymize
    :param file_name: path to file to be modified
    :param subject_id: id to be written in file
    :return:
    """
    with open(file_name, 'rb+') as f:
        # move to subject_id
        f.seek(8)
        f.write('{:<80}'.format(subject_id)[0:80].encode('ascii'))


def bdf_resampler(
              input_file_name: str = None,
              output_path: str = None,
              output_file_name: str = None,
              trash_original: bool = False,
              new_fs: u.Unit = None
              ):

    if output_file_name is None:
        _, _file_name = os.path.split(input_file_name)
        output_file_name = _file_name
    if output_path is None:
        _path, _ = os.path.split(input_file_name)
        output_path = Path(_path)
    data = eeg_reader(file_name=input_file_name)
    print('gathering data from {:}'.format(input_file_name))
    data_original, events_original, units_orignal, annotations_original = data.get_data()
    data_resampled, _factor = eeg_resampling(x=data_original,
                                             new_fs=new_fs,
                                             fs=data.fs)
    et = get_event_times(event_channel=events_original, fs=data.fs)
    events_resampled = events_to_samples_array(events=et, fs=new_fs, n_samples=data_resampled.shape[0])
    Path(output_path).mkdir(parents=True, exist_ok=True)
    _name, _ext = os.path.splitext(output_file_name)
    _output = Path.joinpath(output_path, '{:}_{:}{:}'.format(_name, 'resampled', _ext))

    data_to_bdf(output_file_name=_output,
                data=data_resampled,
                events=events_resampled,
                header=data._header,
                fs=new_fs)

    if trash_original:
        _path, _name = os.path.split(input_file_name)
        _trash_path = Path(_path).joinpath('.trash')
        Path(_trash_path).mkdir(parents=True, exist_ok=True)
        shutil.move(input_file_name, _trash_path.joinpath(_name))
        print('Original file {:} moved to {:}'.format(input_file_name,
                                                      _trash_path.joinpath(_name)))
