
# About
The Python Package Index Project (pypipr)

pypi : https://pypi.org/project/pypipr


# Setup
Install with pip
```
pip install pypipr
```

Then import pypipr
```python
from pypipr import *
# or
import pypipr
```

Or run in terminal/console/cmd/bash
```cmd
pypipr
```

# CONSTANT

`LINUX`

`WINDOWS`

`PintUreg`

# FUNCTION

## avg

`avg(i)`

Simple Average Function karena tidak disediakan oleh python  
  
```python  
n = [1, 22, 2, 3, 13, 2, 123, 12, 31, 2, 2, 12, 2, 1]  
print(avg(n))  
```

Output:
```py
16.285714285714285
```

## basename

`basename(path)`

Mengembalikan nama file dari path  
  
```python  
print(basename("/ini/nama/folder/ke/file.py"))  
```

Output:
```py
file.py
```

## chunk_array

`chunk_array(array, size, start=0)`

Membagi array menjadi potongan-potongan dengan besaran yg diinginkan  
  
```python  
arr = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]  
print(chunk_array(arr, 5))  
print(list(chunk_array(arr, 5)))  
```

Output:
```py
<generator object chunk_array at 0x72f4fd0240>
[[2, 3, 12, 3, 3], [42, 42, 1, 43, 2], [42, 41, 4, 24, 32], [42, 3, 12, 32, 42], [42]]
```

## create_folder

`create_folder(folder_name)`

Membuat folder.  
Membuat folder secara recursive dengan permission.  
  
```py  
create_folder("contoh_membuat_folder")  
create_folder("contoh/membuat/folder/recursive")  
create_folder("./contoh_membuat_folder/secara/recursive")  
```

## datetime_from_string

`datetime_from_string(iso_string, timezone='UTC')`

Parse iso_string menjadi datetime object  
  
```python  
print(datetime_from_string("2022-12-12 15:40:13").isoformat())  
print(datetime_from_string(  
    "2022-12-12 15:40:13",  
    timezone="Asia/Jakarta"  
).isoformat())  
```

Output:
```py
2022-12-12T15:40:13+00:00
2022-12-12T15:40:13+07:00
```

## datetime_now

`datetime_now(timezone=None)`

Memudahkan dalam membuat Datetime untuk suatu timezone tertentu  
  
```python  
print(datetime_now("Asia/Jakarta"))  
print(datetime_now("GMT"))  
print(datetime_now("Etc/GMT+7"))  
```

Output:
```py
2024-04-24 11:39:26.061287+07:00
2024-04-24 04:39:26.061634+00:00
2024-04-23 21:39:26.062212-07:00
```

## dict_first

`dict_first(d: dict, remove=False)`

Mengambil nilai (key, value) pertama dari dictionary dalam bentuk tuple.  
  
```python  
d = {  
    "key2": "value2",  
    "key3": "value3",  
    "key1": "value1",  
}  
print(dict_first(d, remove=True))  
print(dict_first(d))  
```

Output:
```py
('key2', 'value2')
('key3', 'value3')
```

## dirname

`dirname(path)`

Mengembalikan nama folder dari path.  
Tanpa trailing slash di akhir.  
  
```python  
print(dirname("/ini/nama/folder/ke/file.py"))  
```

Output:
```py
/ini/nama/folder/ke
```

## exit_if_empty

`exit_if_empty(*args)`

Keluar dari program apabila seluruh variabel  
setara dengan empty  
  
```py  
var1 = None  
var2 = '0'  
exit_if_empty(var1, var2)  
```

## filter_empty

`filter_empty(iterable, zero_is_empty=True, str_strip=True)`

Mengembalikan iterabel yang hanya memiliki nilai  
  
```python  
var = [1, None, False, 0, "0", True, {}, ['eee']]  
print(filter_empty(var))  
```

Output:
```py
<generator object filter_empty at 0x72f4f66d40>
```

## get_by_index

`get_by_index(obj, index, on_error=None)`

Mendapatkan value dari object berdasarkan indexnya.  
Jika error out of range maka akan mengembalikan on_error.  
  
```python  
l = [1, 3, 5]  
print(get_by_index(l, 7))  
```

Output:
```py
None
```

## get_class_method

`get_class_method(cls)`

Mengembalikan berupa tuple yg berisi list dari method dalam class  
  
```python  
class ExampleGetClassMethod:  
    def a():  
        return [x for x in range(10)]  
  
    def b():  
        return [x for x in range(10)]  
  
    def c():  
        return [x for x in range(10)]  
  
    def d():  
        return [x for x in range(10)]  
  
print(get_class_method(ExampleGetClassMethod))  
print(list(get_class_method(ExampleGetClassMethod)))  
```

Output:
```py
<generator object get_class_method at 0x72f4f67010>
[<function ExampleGetClassMethod.a at 0x730657e7a0>, <function ExampleGetClassMethod.b at 0x72f4fd9580>, <function ExampleGetClassMethod.c at 0x72f4fd9620>, <function ExampleGetClassMethod.d at 0x72f4fd96c0>]
```

## get_filemtime

`get_filemtime(filename)`

Mengambil informasi last modification time file dalam nano seconds  
  
```python  
print(get_filemtime(__file__))  
```

Output:
```py
1710697117516083632
```

## get_filesize

`get_filesize(filename)`

Mengambil informasi file size dalam bytes  
  
```python  
print(get_filesize(__file__))  
```

Output:
```py
465
```

## is_empty

`is_empty(variable, empty=[None, False, 0, 0, '0', '', '-0', '\n', '\t', set(), {}, [], ()])`

Mengecek apakah variable setara dengan nilai kosong pada empty.  
  
Pengecekan nilai yang setara menggunakan simbol '==', sedangkan untuk  
pengecekan lokasi memory yang sama menggunakan keyword 'is'  
  
```python  
print(is_empty("teks"))  
print(is_empty(True))  
print(is_empty(False))  
print(is_empty(None))  
print(is_empty(0))  
print(is_empty([]))  
```

Output:
```py
False
False
True
True
True
True
```

## is_iterable

`is_iterable(var, str_is_iterable=False)`

Mengecek apakah suatu variabel bisa dilakukan forloop atau tidak  
  
```python  
s = 'ini string'  
print(is_iterable(s))  
  
l = [12,21,2,1]  
print(is_iterable(l))  
  
r = range(100)  
print(is_iterable(r))  
  
d = {'a':1, 'b':2}  
print(is_iterable(d.values()))  
```

Output:
```py
False
True
True
True
```

## is_valid_url

`is_valid_url(path)`

Mengecek apakah path merupakan URL yang valid atau tidak.  
Cara ini merupakan cara yang paling efektif.  
  
```python  
print(is_valid_url("https://chat.openai.com/?model=text-davinci-002-render-sha"))  
print(is_valid_url("https://chat.openai.com/?model/=text-dav/inci-002-render-sha"))  
```

Output:
```py
True
True
```

## ivars

`ivars(obj, skip_underscore=True)`

Membuat dictionary berdasarkan kategori untuk setiap  
member dari object.  
  
```python  
iprint(ivars(__import__('pypipr')))  
```

Output:
```py
{'module': {'ibuiltins': <module 'pypipr.ibuiltins' from '/data/data/com.termux/files/home/pypipr/pypipr/ibuiltins/__init__.py'>,
            'iconsole': <module 'pypipr.iconsole' from '/data/data/com.termux/files/home/pypipr/pypipr/iconsole/__init__.py'>,
            'idjango': <module 'pypipr.idjango' from '/data/data/com.termux/files/home/pypipr/pypipr/idjango/__init__.py'>,
            'iengineering': <module 'pypipr.iengineering' from '/data/data/com.termux/files/home/pypipr/pypipr/iengineering/__init__.py'>,
            'ifunctions': <module 'pypipr.ifunctions' from '/data/data/com.termux/files/home/pypipr/pypipr/ifunctions/__init__.py'>,
            'iflow': <module 'pypipr.iflow' (<_frozen_importlib_external.NamespaceLoader object at 0x72f921efd0>)>,
            'asyncio': <module 'asyncio' from '/data/data/com.termux/files/usr/lib/python3.11/asyncio/__init__.py'>,
            'colorama': <module 'colorama' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/colorama/__init__.py'>,
            'datetime': <module 'datetime' from '/data/data/com.termux/files/usr/lib/python3.11/datetime.py'>,
            'functools': <module 'functools' from '/data/data/com.termux/files/usr/lib/python3.11/functools.py'>,
            'inspect': <module 'inspect' from '/data/data/com.termux/files/usr/lib/python3.11/inspect.py'>,
            'io': <module 'io' (frozen)>,
            'json': <module 'json' from '/data/data/com.termux/files/usr/lib/python3.11/json/__init__.py'>,
            'lxml': <module 'lxml' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/lxml/__init__.py'>,
            'math': <module 'math' from '/data/data/com.termux/files/usr/lib/python3.11/lib-dynload/math.cpython-311.so'>,
            'multiprocessing': <module 'multiprocessing' from '/data/data/com.termux/files/usr/lib/python3.11/multiprocessing/__init__.py'>,
            'operator': <module 'operator' from '/data/data/com.termux/files/usr/lib/python3.11/operator.py'>,
            'os': <module 'os' (frozen)>,
            'pathlib': <module 'pathlib' from '/data/data/com.termux/files/usr/lib/python3.11/pathlib.py'>,
            'pint': <module 'pint' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/pint/__init__.py'>,
            'pprint': <module 'pprint' from '/data/data/com.termux/files/usr/lib/python3.11/pprint.py'>,
            'queue': <module 'queue' from '/data/data/com.termux/files/usr/lib/python3.11/queue.py'>,
            'random': <module 'random' from '/data/data/com.termux/files/usr/lib/python3.11/random.py'>,
            're': <module 're' from '/data/data/com.termux/files/usr/lib/python3.11/re/__init__.py'>,
            'requests': <module 'requests' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/requests/__init__.py'>,
            'string': <module 'string' from '/data/data/com.termux/files/usr/lib/python3.11/string.py'>,
            'subprocess': <module 'subprocess' from '/data/data/com.termux/files/usr/lib/python3.11/subprocess.py'>,
            'sys': <module 'sys' (built-in)>,
            'textwrap': <module 'textwrap' from '/data/data/com.termux/files/usr/lib/python3.11/textwrap.py'>,
            'threading': <module 'threading' from '/data/data/com.termux/files/usr/lib/python3.11/threading.py'>,
            'time': <module 'time' (built-in)>,
            'tzdata': <module 'tzdata' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/tzdata/__init__.py'>,
            'uuid': <module 'uuid' from '/data/data/com.termux/files/usr/lib/python3.11/uuid.py'>,
            'webbrowser': <module 'webbrowser' from '/data/data/com.termux/files/usr/lib/python3.11/webbrowser.py'>,
            'yaml': <module 'yaml' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/yaml/__init__.py'>,
            'zoneinfo': <module 'zoneinfo' from '/data/data/com.termux/files/usr/lib/python3.11/zoneinfo/__init__.py'>},
 'class': {'ComparePerformance': <class 'pypipr.ibuiltins.ComparePerformance.ComparePerformance'>,
           'RunParallel': <class 'pypipr.ibuiltins.RunParallel.RunParallel'>,
           'APIMixinView': <class 'pypipr.idjango.APIMixinView.APIMixinView'>,
           'PintUregQuantity': <class 'pint.Quantity'>},
 'variable': {'LINUX': True,
              'WINDOWS': False,
              'PintUreg': <pint.registry.UnitRegistry object at 0x7302ccb1d0>},
 'function': {'avg': <function avg at 0x73065b6d40>,
              'basename': <function basename at 0x730657e8e0>,
              'chunk_array': <function chunk_array at 0x7302c01120>,
              'create_folder': <function create_folder at 0x7302c01300>,
              'datetime_from_string': <function datetime_from_string at 0x7302c014e0>,
              'datetime_now': <function datetime_now at 0x7302ca9620>,
              'dict_first': <function dict_first at 0x7302ca9580>,
              'dirname': <function dirname at 0x7302ca94e0>,
              'exit_if_empty': <function exit_if_empty at 0x7302c834c0>,
              'filter_empty': <function filter_empty at 0x7302ca91c0>,
              'get_by_index': <function get_by_index at 0x7302ca8ea0>,
              'get_class_method': <function get_class_method at 0x7302ca8cc0>,
              'get_filemtime': <function get_filemtime at 0x7302ca8b80>,
              'get_filesize': <function get_filesize at 0x7302ca89a0>,
              'is_empty': <function is_empty at 0x7302ca9260>,
              'is_iterable': <function is_iterable at 0x7302ca8fe0>,
              'is_valid_url': <function is_valid_url at 0x7302ca8860>,
              'ivars': <function ivars at 0x7302ca87c0>,
              'password_generator': <function password_generator at 0x7302ca8680>,
              'random_bool': <function random_bool at 0x7302ca8400>,
              'set_timeout': <function set_timeout at 0x7302cab7e0>,
              'sets_ordered': <function sets_ordered at 0x7302cab920>,
              'str_cmp': <function str_cmp at 0x7302cab9c0>,
              'to_str': <function to_str at 0x7302ca8f40>,
              'choices': <function choices at 0x7302caba60>,
              'console_run': <function console_run at 0x7302cabce0>,
              'input_char': <function input_char at 0x7302cabe20>,
              'log': <function log at 0x7302cd0040>,
              'print_colorize': <function print_colorize at 0x7302cd00e0>,
              'print_dir': <function print_dir at 0x7302cd0220>,
              'print_log': <function print_log at 0x7302cabec0>,
              'print_to_last_line': <function print_to_last_line at 0x7302cabc40>,
              'text_colorize': <function text_colorize at 0x7302cabd80>,
              'batch_calculate': <function batch_calculate at 0x72f9235580>,
              'batchmaker': <function batchmaker at 0x72f920e980>,
              'calculate': <function calculate at 0x72f92362a0>,
              'auto_reload': <function auto_reload at 0x72f9236480>,
              'github_pull': <function github_pull at 0x72f9236020>,
              'github_push': <function github_push at 0x72f9236700>,
              'github_user': <function github_user at 0x72f9236a20>,
              'pip_freeze_without_version': <function pip_freeze_without_version at 0x72f8f5a020>,
              'poetry_publish': <function poetry_publish at 0x72f8f5a160>,
              'poetry_update_version': <function poetry_update_version at 0x72f8f7a980>,
              'iargv': <function iargv at 0x72f51a00e0>,
              'idumps': <function idumps at 0x72f51a0220>,
              'idumps_html': <function idumps_html at 0x72f5204c20>,
              'ienv': <function ienv at 0x72f51a0360>,
              'iexec': <function iexec at 0x72f5204ea0>,
              'ijoin': <function ijoin at 0x72f8f59ee0>,
              'iloads': <function iloads at 0x72f5204f40>,
              'iloads_html': <function iloads_html at 0x72f52051c0>,
              'iopen': <function iopen at 0x72f8f5a200>,
              'iprint': <function iprint at 0x72f51a0180>,
              'irange': <function irange at 0x72f92363e0>,
              'ireplace': <function ireplace at 0x72f5205080>,
              'iscandir': <function iscandir at 0x72f5206e80>,
              'isplit': <function isplit at 0x72f5206f20>}}
```

## password_generator

`password_generator(length=8, characters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')`

Membuat pssword secara acak  
  
```python  
print(password_generator())  
```

Output:
```py
Uy}-6-Qh
```

## random_bool

`random_bool()`

Menghasilkan nilai random True atau False.  
Fungsi ini merupakan fungsi tercepat untuk mendapatkan random bool.  
Fungsi ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan  
overhead yg besar.  
  
```python  
print(random_bool())  
```

Output:
```py
True
```

## set_timeout

`set_timeout(interval, func, args=None, kwargs=None)`

Menjalankan fungsi ketika sudah sekian detik.  
Apabila timeout masih berjalan tapi kode sudah selesai dieksekusi semua, maka  
program tidak akan berhenti sampai timeout selesai, kemudian fungsi dijalankan,  
kemudian program dihentikan.  
  
```python  
set_timeout(3, lambda: print("Timeout 3"))  
x = set_timeout(7, print, args=["Timeout 7"])  
print(x)  
print("menghentikan timeout 7")  
x.cancel()  
```

Output:
```py
<Timer(Thread-2, started 493713603824)>
menghentikan timeout 7
```

## sets_ordered

`sets_ordered(iterator)`

Hanya mengambil nilai unik dari suatu list  
  
```python  
array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]  
print(sets_ordered(array))  
print(list(sets_ordered(array)))  
```

Output:
```py
<generator object sets_ordered at 0x72f4fe41e0>
[2, 3, 12, 42, 1, 43, 41, 4, 24, 32]
```

## str_cmp

`str_cmp(t1, t2)`

Membandingakan string secara incase-sensitive menggunakan lower().  
Lebih cepat dibandingkan upper(), casefold(), re.fullmatch(), len().  
perbandingan ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan  
overhead yg besar.  
  
```python  
print(str_cmp('teks1', 'Teks1'))  
```

Output:
```py
True
```

## to_str

`to_str(value)`

Mengubah value menjadi string literal  
  
```python  
print(to_str(5))  
print(to_str([]))  
print(to_str(False))  
print(to_str(True))  
print(to_str(None))  
```

Output:
```py
5

False
True

```

## choices

`choices(iterator, title=None, prompt='', default=None)`

Memudahkan dalam membuat pilihan untuk user dalam tampilan console  
  
```py  
a = choices("ini hanya satu pilihan")  
b = choices(  
    {  
        "sedan": "audi",  
        "suv": "volvo",  
        "truck": "tesla",  
    },  
    title="Car Model",  
    prompt="Pilih Mobil : ",  
)  
c = choices(  
    iscandir(recursive=False),  
    title="List File dan Folder",  
    prompt="Pilih File atau Folder : ",  
)  
```

## console_run

`console_run(info, command=None, print_info=True, capture_output=False)`

Menjalankan command seperti menjalankan command di Command Terminal  
  
```py  
console_run('dir')  
console_run('ls')  
```

## input_char

`input_char(prompt=None, prompt_ending='', newline_after_input=True, echo_char=True, default=None)`

Meminta masukan satu huruf tanpa menekan Enter.  
  
```py  
input_char("Input char : ")  
input_char("Input char : ", default='Y')  
input_char("Input Char without print : ", echo_char=False)  
```

## log

`log(text=None)`

Decorator untuk mempermudah pembuatan log karena tidak perlu mengubah  
fungsi yg sudah ada.  
Melakukan print ke console untuk menginformasikan proses yg sedang  
berjalan didalam program.  
  
```py  
@log  
def some_function():  
    pass  
  
@log()  
def some_function_again():  
    pass  
  
@log("Calling some function")  
def some_function_more():  
    pass  
  
some_function()  
some_function_again()  
some_function_more()  
```

## print_colorize

`print_colorize(text, color='\x1b[32m', bright='\x1b[1m', color_end='\x1b[0m', text_start='', text_end='\n')`

Print text dengan warna untuk menunjukan text penting  
  
```py  
print_colorize("Print some text")  
print_colorize("Print some text", color=colorama.Fore.RED)  
```

## print_dir

`print_dir(var, colorize=True)`

Print property dan method yang tersedia pada variabel  
  
```python  
import pathlib  
p = pathlib.Path("https://www.google.com/")  
print_dir(p, colorize=False)  
```

Output:
```py
           __bytes__ : b'https:/www.google.com'
           __class__ : .
             __dir__ : ['__module__', '__doc__', '__slots__', '__new__', '_make_child_relpath', '__enter__', '__exit__', 'cwd', 'home', 'samefile', 'iterdir', '_scandir', 'glob', 'rglob', 'absolute', 'resolve', 'stat', 'owner', 'group', 'open', 'read_bytes', 'read_text', 'write_bytes', 'write_text', 'readlink', 'touch', 'mkdir', 'chmod', 'lchmod', 'unlink', 'rmdir', 'lstat', 'rename', 'replace', 'symlink_to', 'hardlink_to', 'link_to', 'exists', 'is_dir', 'is_file', 'is_mount', 'is_symlink', 'is_block_device', 'is_char_device', 'is_fifo', 'is_socket', 'expanduser', '__reduce__', '_parse_args', '_from_parts', '_from_parsed_parts', '_format_parsed_parts', '_make_child', '__str__', '__fspath__', 'as_posix', '__bytes__', '__repr__', 'as_uri', '_cparts', '__eq__', '__hash__', '__lt__', '__le__', '__gt__', '__ge__', 'drive', 'root', 'anchor', 'name', 'suffix', 'suffixes', 'stem', 'with_name', 'with_stem', 'with_suffix', 'relative_to', 'is_relative_to', 'parts', 'joinpath', '__truediv__', '__rtruediv__', 'parent', 'parents', 'is_absolute', 'is_reserved', 'match', '_cached_cparts', '_drv', '_hash', '_parts', '_pparts', '_root', '_str', '__getattribute__', '__setattr__', '__delattr__', '__ne__', '__init__', '__reduce_ex__', '__getstate__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__', '_flavour']
             __doc__ : Path subclass for non-Windows systems.

    On a POSIX system, instantiating a Path should return this object.
    
           __enter__ : https:/www.google.com
          __fspath__ : https:/www.google.com
        __getstate__ : (None, {'_drv': '', '_root': '', '_parts': ['https:', 'www.google.com'], '_str': 'https:/www.google.com'})
            __hash__ : 1324913689339074732
            __init__ : None
   __init_subclass__ : None
          __module__ : pathlib
          __reduce__ : (<class 'pathlib.PosixPath'>, ('https:', 'www.google.com'))
            __repr__ : PosixPath('https:/www.google.com')
          __sizeof__ : 72
           __slots__ : ()
             __str__ : https:/www.google.com
    __subclasshook__ : NotImplemented
      _cached_cparts : ['https:', 'www.google.com']
             _cparts : ['https:', 'www.google.com']
                _drv : 
            _flavour : <pathlib._PosixFlavour object at 0x7302c7c2d0>
               _hash : 1324913689339074732
              _parts : ['https:', 'www.google.com']
               _root : 
                _str : https:/www.google.com
            absolute : /data/data/com.termux/files/home/pypipr/https:/www.google.com
              anchor : 
            as_posix : https:/www.google.com
                 cwd : /data/data/com.termux/files/home/pypipr
               drive : 
              exists : False
          expanduser : https:/www.google.com
                home : /data/data/com.termux/files/home
         is_absolute : False
     is_block_device : False
      is_char_device : False
              is_dir : False
             is_fifo : False
             is_file : False
            is_mount : False
         is_reserved : False
           is_socket : False
          is_symlink : False
             iterdir : <generator object Path.iterdir at 0x72f4fbcc80>
            joinpath : https:/www.google.com
                name : www.google.com
              parent : https:
             parents : <PosixPath.parents>
               parts : ('https:', 'www.google.com')
             resolve : /data/data/com.termux/files/home/pypipr/https:/www.google.com
                root : 
                stem : www.google
              suffix : .com
            suffixes : ['.google', '.com']
```

## print_log

`print_log(text)`

Akan melakukan print ke console.  
Berguna untuk memberikan informasi proses program yg sedang berjalan.  
  
```python  
print_log("Standalone Log")  
```

Output:
```py
[32m[1m>>> Standalone Log[0m
```

## print_to_last_line

`print_to_last_line(text: str, latest=1, clear=True)`

Melakukan print ke konsol tetapi akan menimpa baris terakhir.  
Berguna untuk memberikan progress secara interaktif.  
  
```py  
c = input("masukkan apa saja : ")  
print_to_last_line(f"masukkan apa saja : {c} [ok]")  
```

## text_colorize

`text_colorize(text, color='\x1b[32m', bright='\x1b[1m', color_end='\x1b[0m')`

return text dengan warna untuk menunjukan text penting  
  
```py  
text_colorize("Print some text")  
text_colorize("Print some text", color=colorama.Fore.RED)  
```

## batch_calculate

`batch_calculate(pattern)`

Analisa perhitungan massal.  
Bisa digunakan untuk mencari alternatif terendah/tertinggi/dsb.  
  
  
```python  
print(batch_calculate("{1 10} m ** {1 3}"))  
print(list(batch_calculate("{1 10} m ** {1 3}")))  
```

Output:
```py
<generator object batch_calculate at 0x72f4f67b50>
[('1 m ** 1', <Quantity(1, 'meter')>), ('1 m ** 2', <Quantity(1, 'meter ** 2')>), ('1 m ** 3', <Quantity(1, 'meter ** 3')>), ('2 m ** 1', <Quantity(2, 'meter')>), ('2 m ** 2', <Quantity(2, 'meter ** 2')>), ('2 m ** 3', <Quantity(2, 'meter ** 3')>), ('3 m ** 1', <Quantity(3, 'meter')>), ('3 m ** 2', <Quantity(3, 'meter ** 2')>), ('3 m ** 3', <Quantity(3, 'meter ** 3')>), ('4 m ** 1', <Quantity(4, 'meter')>), ('4 m ** 2', <Quantity(4, 'meter ** 2')>), ('4 m ** 3', <Quantity(4, 'meter ** 3')>), ('5 m ** 1', <Quantity(5, 'meter')>), ('5 m ** 2', <Quantity(5, 'meter ** 2')>), ('5 m ** 3', <Quantity(5, 'meter ** 3')>), ('6 m ** 1', <Quantity(6, 'meter')>), ('6 m ** 2', <Quantity(6, 'meter ** 2')>), ('6 m ** 3', <Quantity(6, 'meter ** 3')>), ('7 m ** 1', <Quantity(7, 'meter')>), ('7 m ** 2', <Quantity(7, 'meter ** 2')>), ('7 m ** 3', <Quantity(7, 'meter ** 3')>), ('8 m ** 1', <Quantity(8, 'meter')>), ('8 m ** 2', <Quantity(8, 'meter ** 2')>), ('8 m ** 3', <Quantity(8, 'meter ** 3')>), ('9 m ** 1', <Quantity(9, 'meter')>), ('9 m ** 2', <Quantity(9, 'meter ** 2')>), ('9 m ** 3', <Quantity(9, 'meter ** 3')>), ('10 m ** 1', <Quantity(10, 'meter')>), ('10 m ** 2', <Quantity(10, 'meter ** 2')>), ('10 m ** 3', <Quantity(10, 'meter ** 3')>)]
```

## batchmaker

`batchmaker(pattern: str)`

Alat Bantu untuk membuat teks yang berulang.  
Gunakan `{[start][separator][finish]([separator][step])}`.  
```  
[start] dan [finish]    -> bisa berupa huruf maupun angka  
([separator][step])     -> bersifat optional  
[separator]             -> selain huruf dan angka  
[step]                  -> berupa angka positif  
```  
  
```python  
s = "Urutan {1/6/3} dan {10:9} dan {j k} dan {Z - A - 15} saja."  
print(batchmaker(s))  
print(list(batchmaker(s)))  
```

Output:
```py
<generator object batchmaker at 0x72f4fd4040>
['Urutan 1 dan 10 dan j dan Z saja.', 'Urutan 1 dan 10 dan j dan K saja.', 'Urutan 1 dan 10 dan k dan Z saja.', 'Urutan 1 dan 10 dan k dan K saja.', 'Urutan 1 dan 9 dan j dan Z saja.', 'Urutan 1 dan 9 dan j dan K saja.', 'Urutan 1 dan 9 dan k dan Z saja.', 'Urutan 1 dan 9 dan k dan K saja.', 'Urutan 4 dan 10 dan j dan Z saja.', 'Urutan 4 dan 10 dan j dan K saja.', 'Urutan 4 dan 10 dan k dan Z saja.', 'Urutan 4 dan 10 dan k dan K saja.', 'Urutan 4 dan 9 dan j dan Z saja.', 'Urutan 4 dan 9 dan j dan K saja.', 'Urutan 4 dan 9 dan k dan Z saja.', 'Urutan 4 dan 9 dan k dan K saja.']
```

## calculate

`calculate(teks)`

Mengembalikan hasil dari perhitungan teks menggunakan modul pint.  
Mendukung perhitungan matematika dasar dengan satuan.  
  
Return value:  
- Berupa class Quantity dari modul pint  
  
Format:  
- f"{result:~P}"            -> pretty  
- f"{result:~H}"            -> html  
- result.to_base_units()    -> SI  
- result.to_compact()       -> human readable  
  
```python  
fx = "3 meter * 10 cm * 3 km"  
res = calculate(fx)  
print(res)  
print(res.to_base_units())  
print(res.to_compact())  
print(f"{res:~P}")  
print(f"{res:~H}")  
```

Output:
```py
90 centimeter * kilometer * meter
900.0 meter ** 3
900.0 meter ** 3
90 cm·km·m
90 cm km m
```

## auto_reload

`auto_reload(filename)`

Menjalankan file python secara berulang.  
Dengan tujuan untuk melihat perubahan secara langsung.  
Pastikan kode aman untuk dijalankan.  
Jalankan kode ini di terminal console.  
  
```py  
if __name__ == "__main__":  
    auto_reload("file_name.py")  
```

## github_pull

`github_pull()`

Menjalankan command `git pull`  
  
```py  
github_pull()  
```

## github_push

`github_push(commit_msg=None)`

Menjalankan command status, add, commit dan push  
  
```py  
github_push('Commit Message')  
```

## github_user

`github_user(email=None, name=None)`

Menyimpan email dan nama user secara global sehingga tidak perlu  
menginput nya setiap saat.  
  
```py  
github_user('my@emil.com', 'MyName')  
```

## pip_freeze_without_version

`pip_freeze_without_version(filename=None)`

Memberikan list dari dependencies yang terinstall tanpa version.  
Bertujuan untuk menggunakan Batteries Included Python.  
  
```py  
print(pip_freeze_without_version())  
```

## poetry_publish

`poetry_publish(token=None)`

Publish project to pypi,org  
  
```py  
poetry_publish()  
```

## poetry_update_version

`poetry_update_version(mayor=False, minor=False, patch=False)`

Update versi pada pyproject.toml menggunakan poetry  
  
```py  
poetry_update_version()  
```

## iargv

`iargv(key: int, cast=None, on_error=None)`

Mengambil parameter input dari terminal tanpa menimbulkan error  
apabila parameter kosong.  
Parameter yg berupa string juga dapat diubah menggunakan cast.  
  
```python  
if __name__ == "__main__":  
    print(iargv(1, cast=int, on_error=100))  
```

Output:
```py
```

## idumps

`idumps(data, syntax='yaml', indent=4)`

Mengubah variabel data menjadi string untuk yang dapat dibaca untuk disimpan.  
String yang dihasilkan berbentuk syntax YAML/JSON/HTML.  
  
```python  
data = {  
    'a': 123,  
    't': ['disini', 'senang', 'disana', 'senang'],  
    'l': (12, 23, [12, 42]),  
}  
print(idumps(data))  
print(idumps(data, syntax='html'))  
```

Output:
```py
a: 123
l: !!python/tuple
- 12
- 23
-   - 12
    - 42
t:
- disini
- senang
- disana
- senang

<table>
    <tbody>
        <tr>
            <th>a</th>
            <td>
                <span>123</span>
            </td>
        </tr>
        <tr>
            <th>t</th>
            <td>
                <ul>
                    <li>
                        <span>disini</span>
                    </li>
                    <li>
                        <span>senang</span>
                    </li>
                    <li>
                        <span>disana</span>
                    </li>
                    <li>
                        <span>senang</span>
                    </li>
                </ul>
            </td>
        </tr>
        <tr>
            <th>l</th>
            <td>
                <ul>
                    <li>
                        <span>12</span>
                    </li>
                    <li>
                        <span>23</span>
                    </li>
                    <li>
                        <ul>
                            <li>
                                <span>12</span>
                            </li>
                            <li>
                                <span>42</span>
                            </li>
                        </ul>
                    </li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

```

## idumps_html

`idumps_html(data, indent=None)`

Serialisasi python variabel menjadi HTML.  
```  
List -> <ul>...</ul>  
Dict -> <table>...</table>  
```  
  
```python  
data = {  
    'abc': 123,  
    'list': [1, 2, 3, 4, 5],  
    'dict': {'a': 1, 'b':2, 'c':3},  
}  
print(idumps_html(data))  
```

Output:
```py
<table>
  <tbody>
    <tr>
      <th>abc</th>
      <td>
        <span>123</span>
      </td>
    </tr>
    <tr>
      <th>list</th>
      <td>
        <ul>
          <li>
            <span>1</span>
          </li>
          <li>
            <span>2</span>
          </li>
          <li>
            <span>3</span>
          </li>
          <li>
            <span>4</span>
          </li>
          <li>
            <span>5</span>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <th>dict</th>
      <td>
        <table>
          <tbody>
            <tr>
              <th>a</th>
              <td>
                <span>1</span>
              </td>
            </tr>
            <tr>
              <th>b</th>
              <td>
                <span>2</span>
              </td>
            </tr>
            <tr>
              <th>c</th>
              <td>
                <span>3</span>
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>

```

## ienv

`ienv(on_windows=None, on_linux=None)`

Mengambalikan hasil berdasarkan environment dimana program dijalankan  
  
```py  
getch = __import__(ienv(on_windows="msvcrt", on_linux="getch"))  
  
  
f = ienv(on_windows=fwin, on_linux=flin)  
f()  
  
  
inherit = ienv(  
    on_windows=[BaseForWindows, BaseEnv, object],  
    on_linux=[SpecialForLinux, BaseForLinux, BaseEnv, object]  
)  
  
class ExampleIEnv(*inherit):  
    pass  
```

## iexec

`iexec(python_syntax, import_pypipr=True)`

improve exec() python function untuk mendapatkan outputnya  
  
```python  
print(iexec('print(9*9)'))  
```

Output:
```py
81

```

## ijoin

`ijoin(iterable, separator='', start='', end='', remove_empty=False, recursive=True, recursive_flat=False, str_strip=False)`

Simplify Python join functions like PHP function.  
Iterable bisa berupa sets, tuple, list, dictionary.  
  
```python  
arr = {'asd','dfs','weq','qweqw'}  
print(ijoin(arr, ', '))  
  
arr = '/ini/path/seperti/url/'.split('/')  
print(ijoin(arr, ','))  
print(ijoin(arr, ',', remove_empty=True))  
  
arr = {'a':'satu', 'b':(12, 34, 56), 'c':'tiga', 'd':'empat'}  
print(ijoin(arr, separator='</li>\n<li>', start='<li>', end='</li>',  
    recursive_flat=True))  
print(ijoin(arr, separator='</div>\n<div>', start='<div>', end='</div>'))  
print(ijoin(10, ' '))  
```

Output:
```py
dfs, weq, qweqw, asd
,ini,path,seperti,url,
ini,path,seperti,url
<li>satu</li>
<li>12</li>
<li>34</li>
<li>56</li>
<li>tiga</li>
<li>empat</li>
<div>satu</div>
<div><div>12</div>
<div>34</div>
<div>56</div></div>
<div>tiga</div>
<div>empat</div>
10
```

## iloads

`iloads(data, syntax='yaml')`

Mengubah string data hasil dari idumps menjadi variabel.  
String data adalah berupa syntax YAML.  
  
```python  
data = {  
    'a': 123,  
    't': ['disini', 'senang', 'disana', 'senang'],  
    'l': (12, 23, [12, 42]),  
}  
s = idumps(data)  
print(iloads(s))  
```

Output:
```py
{'a': 123, 'l': (12, 23, [12, 42]), 't': ['disini', 'senang', 'disana', 'senang']}
```

## iloads_html

`iloads_html(html)`

Mengambil data yang berupa list `<ul>`, dan table `<table>` dari html  
dan menjadikannya data python berupa list.  
setiap data yang ditemukan akan dibungkus dengan tuple sebagai separator.  
```  
list (<ul>)     -> list         -> list satu dimensi  
table (<table>) -> list[list]   -> list satu dimensi didalam list  
```  
apabila data berupa ul maka dapat dicek type(data) -> html_ul  
apabila data berupa ol maka dapat dicek type(data) -> html_ol  
apabila data berupa dl maka dapat dicek type(data) -> html_dl  
apabila data berupa table maka dapat dicek type(data) -> html_table  
  
```python  
import pprint  
pprint.pprint(iloads_html(iopen("https://harga-emas.org/")), depth=10)  
pprint.pprint(iloads_html(iopen("https://harga-emas.org/1-gram/")), depth=10)  
```

Output:
```py
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram', 'Pluang'],
 [['Harga Emas Hari Ini - Rabu, 24 April 2024'],
  ['Spot Emas USD↓2.327,60 (-2,31) / oz',
   'Kurs IDR↑16.244,00 (+20,00) / USD',
   'Emas IDR↑1.215.605 (+292) / gr'],
  ['LM Antam (Jual)↓1.320.000 (-5.000) / gr',
   'LM Antam (Beli)↓1.218.000 (-5.000) / gr']],
 [['Harga Emas Hari Ini'],
  ['Gram', 'Gedung Antam Jakarta', 'Pegadaian'],
  ['per Gram (Rp)', 'per Batangan (Rp)', 'per Gram (Rp)', 'per Batangan (Rp)'],
  ['1000',
   '1.261 (-5)',
   '1.260.600 (-5.000)',
   '1.043.040 (+8.200)',
   '1.043.040.000 (+8.200.000)'],
  ['500',
   '2.521 (-10)',
   '1.260.640 (-5.000)',
   '1.043.082 (+8.200)',
   '521.541.000 (+4.100.000)'],
  ['250',
   '5.044 (-20)',
   '1.261.060 (-5.000)',
   '1.043.512 (+8.200)',
   '260.878.000 (+2.050.000)'],
  ['100',
   '12.621 (-50)',
   '1.262.120 (-5.000)',
   '1.044.600 (+8.200)',
   '104.460.000 (+820.000)'],
  ['50',
   '25.258 (-100)',
   '1.262.900 (-5.000)',
   '1.045.400 (+8.200)',
   '52.270.000 (+410.000)'],
  ['25',
   '50.579 (-200)',
   '1.264.480 (-5.000)',
   '1.047.040 (+8.200)',
   '26.176.000 (+205.000)'],
  ['10',
   '126.950 (-500)',
   '1.269.500 (-5.000)',
   '1.052.200 (+8.200)',
   '10.522.000 (+82.000)'],
  ['5',
   '255.000 (-1.000)',
   '1.275.000 (-5.000)',
   '1.057.800 (+8.200)',
   '5.289.000 (+41.000)'],
  ['3',
   '427.222 (-1.667)',
   '1.281.667 (-5.000)',
   '1.064.667 (+8.000)',
   '3.194.000 (+24.000)'],
  ['2',
   '645.000 (-2.500)',
   '1.290.000 (-5.000)',
   '1.073.500 (+8.500)',
   '2.147.000 (+17.000)'],
  ['1',
   '1.320.000 (-5.000)',
   '1.320.000 (-5.000)',
   '1.104.000 (+8.000)',
   '1.104.000 (+8.000)'],
  ['0.5',
   '2.840.000 (-10.000)',
   '1.420.000 (-5.000)',
   '1.208.000 (+8.000)',
   '604.000 (+4.000)'],
  ['Update harga LM Antam :24 April 2024, pukul 08:12Harga pembelian kembali '
   ':Rp. 1.218.000/gram (-5.000)',
   'Update harga LM Pegadaian :31 Agustus 2023']],
 [['Spot Harga Emas Hari Ini (Market Open)'],
  ['Satuan', 'USD', 'Kurs\xa0Dollar', 'IDR'],
  ['Ounce\xa0(oz)', '2.327,60 (-2,31)', '16.244,00 (+20,00)', '37.809.534'],
  ['Gram\xa0(gr)', '74,83', '16.244,00', '1.215.605 (+292)'],
  ['Kilogram\xa0(kg)', '74.834,08', '16.244,00', '1.215.604.760'],
  ['Update harga emas :24 April 2024, pukul 11:39Update kurs :24 April 2024, '
   'pukul 09:10']],
 [['Gram', 'UBS Gold 99.99%'],
  ['Jual', 'Beli'],
  ['/ Batang', '/ Gram', '/ Batang', '/ Gram'],
  ['100',
   '126.212.000 (-500.000)',
   '1.262.120 (-5.000)',
   '123.735.000',
   '1.237.350'],
  ['50',
   '63.145.000 (-250.000)',
   '1.262.900 (-5.000)',
   '61.920.000',
   '1.238.400'],
  ['25',
   '31.612.000 (-125.000)',
   '1.264.480 (-5.000)',
   '31.062.500',
   '1.242.500'],
  ['10',
   '12.695.000 (-50.000)',
   '1.269.500 (-5.000)',
   '12.475.000',
   '1.247.500'],
  ['5', '6.375.000 (-25.000)', '1.275.000 (-5.000)', '6.289.500', '1.257.900'],
  ['1', '1.320.000 (-5.000)', '1.320.000 (-5.000)', '1.290.500', '1.290.500'],
  ['', 'Update :24 April 2024, pukul 10:55']],
 [['Konversi Satuan'],
  ['Satuan', 'Ounce (oz)', 'Gram (gr)', 'Kilogram (kg)'],
  ['Ounce\xa0(oz)', '1', '31,1034767696', '0,0311034768'],
  ['Gram\xa0(gr)', '0,0321507466', '1', '0.001'],
  ['Kilogram\xa0(kg)', '32,1507466000', '1.000', '1']],
 [['Pergerakan Harga Emas Dunia'],
  ['Waktu', 'Emas'],
  ['Unit', 'USD', 'IDR'],
  ['Angka', '+/-', 'Angka', '+/-'],
  ['Hari Ini', 'Kurs', '', '', '16.224', '+20+0,12%'],
  ['oz', '2.329,91', '-2,31-0,10%', '37.800.460', '+9.075+0,02%'],
  ['gr', '74,91', '-0,07-0,10%', '1.215.313', '+292+0,02%'],
  ['30 Hari', 'Kurs', '', '', '15.773', '+471+2,99%'],
  ['oz', '2.175,55', '+152,05+6,99%', '34.314.950', '+3.494.584+10,18%'],
  ['gr', '69,95', '+4,89+6,99%', '1.103.251', '+112.353+10,18%'],
  ['2 Bulan', 'Kurs', '', '', '15.630', '+614+3,93%'],
  ['oz', '2.035,57', '+292,03+14,35%', '31.815.959', '+5.993.575+18,84%'],
  ['gr', '65,45', '+9,39+14,35', '1.022.907', '+192.698+18,84%'],
  ['6 Bulan', 'Kurs', '', '', '15.933', '+311+1,95%'],
  ['oz', '1.983,13', '+344,47+17,37%', '31.597.210', '+6.212.324+19,66%'],
  ['gr', '63,76', '+11,07+17,37%', '1.015.874', '+199.731+19,66%'],
  ['1 Tahun', 'Kurs', '', '', '15.731', '+513+3,26%'],
  ['oz', '1.823,86', '+503,74+27,62%', '28.691.142', '+9.118.393+31,78%'],
  ['gr', '58,64', '+16,20+27,62%', '922.442', '+293.163+31,78%'],
  ['2 Tahun', 'Kurs', '', '', '14.361', '+1.883+13,11%'],
  ['oz', '1.896,13', '+431,47+22,76%', '27.230.342', '+10.579.193+38,85%'],
  ['gr', '60,96', '+13,87+22,76%', '875.476', '+340.129+38,85%'],
  ['3 Tahun', 'Kurs', '', '', '14.530', '+1.714+11,80%'],
  ['oz', '1.777,11', '+550,49+30,98%', '25.821.408', '+11.988.126+46,43%'],
  ['gr', '57,14', '+17,70+30,98%', '830.178', '+385.427+46,43%'],
  ['5 Tahun', 'Kurs', '', '', '14.188', '+2.056+14,49%'],
  ['oz', '1.288,10', '+1.039,50+80,70%', '18.275.563', '+19.533.972+106,89%'],
  ['gr', '41,41', '+33,42+80,70%', '587.573', '+628.032+106,89%']])
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram', 'Pluang'],
 [[''],
  ['Emas 24 KaratHarga Emas 1 Gram', ''],
  ['USD', '74,83↓', '-0,08-0,11%'],
  ['KURS', '16.151,15↑', '+4,25+0,03%'],
  ['IDR', '1.208.656,42↓', '-881,15-0,07%'],
  ['Rabu, 24 April 2024 11:39']],
 [[''],
  ['Emas 1 Gram (IDR)Emas 1 Gram (USD)Kurs USD-IDR',
   'Hari Ini',
   '1 Bulan',
   '1 Tahun',
   '5 Tahun',
   'Max',
   '']],
 [['Pergerakkan Harga Emas 1 Gram'],
  ['', 'Penutupan Kemarin', 'Pergerakkan Hari Ini', 'Rata-rata'],
  ['USD', '74,91', '74,83 - 74,91', '74,87'],
  ['KURS', '16.146,90', '16.146,90 - 16.151,15', '16.149,03'],
  ['IDR', '1.209.537,57', '1.208.656,42 - 1.209.537,57', '1.209.097,00'],
  [''],
  ['', 'Awal Tahun', 'Pergerakkan YTD', '+/- YTD'],
  ['USD', '66,32', '64,07 - 77,14', '+8,51 (12,83%)'],
  ['KURS', '15.390,10', '15.390,00 - 16.307,80', '+761,05 (4,95%)'],
  ['IDR', '1.020.729,53', '997.660,12 - 1.256.829,06', '+187.926,89 (18,41%)'],
  [''],
  ['', 'Tahun Lalu / 52 Minggu', 'Pergerakkan 52 Minggu', '+/- 52 Minggu'],
  ['USD', '63,76', '58,43 - 77,14', '+11,07 (17,36%)'],
  ['KURS', '14.936,00', '14.669,40 - 16.307,80', '+1.215,15 (8,14%)'],
  ['IDR', '952.339,68', '912.925,68 - 1.256.829,06', '+256.316,74 (26,91%)']])
```

## iopen

`iopen(path, data=None, regex=None, css_select=None, xpath=None, file_append=False)`

Membaca atau Tulis pada path yang bisa merupakan FILE maupun URL.  
  
Baca File :  
- Membaca seluruh file.  
- Jika berhasil content dapat diparse dengan regex.  
- Apabila File berupa html, dapat diparse dengan css atau xpath.  
  
Tulis File :  
- Menulis pada file.  
- Jika file tidak ada maka akan dibuat.  
- Jika file memiliki content maka akan di overwrite.  
  
Membaca URL :  
- Mengakses URL dan mengembalikan isi html nya berupa teks.  
- Content dapat diparse dengan regex, css atau xpath.  
  
Tulis URL :  
- Mengirimkan data dengan metode POST ke url.  
- Jika berhasil dan response memiliki content, maka dapat diparse  
  dengan regex, css atau xpath.  
  
  
```python  
# FILE  
print(iopen("__iopen.txt", "mana aja"))  
print(iopen("__iopen.txt", regex="(\w+)"))  
# URL  
print(iopen("https://www.google.com/", css_select="a"))  
print(iopen("https://www.google.com/", dict(coba="dulu"), xpath="//a"))  
```

Output:
```py
8
['mana', 'aja']
[<Element a at 0x72f4fc6f80>, <Element a at 0x72f5012670>, <Element a at 0x72f5012710>, <Element a at 0x72f5012760>, <Element a at 0x72f50127b0>, <Element a at 0x72f5012800>, <Element a at 0x72f5012850>, <Element a at 0x72f50128a0>, <Element a at 0x72f50128f0>, <Element a at 0x72f5012940>, <Element a at 0x72f5012990>, <Element a at 0x72f50129e0>, <Element a at 0x72f5012a30>, <Element a at 0x72f5012a80>, <Element a at 0x72f5012ad0>, <Element a at 0x72f5012b20>, <Element a at 0x72f5012b70>, <Element a at 0x72f5012bc0>]
False
```

## iprint

`iprint(*args, color=None, sort_dicts=False, **kwargs)`

Improve print function dengan menambahkan color dan pretty print  
Color menggunakan colorama Fore + Back + Style  
  
```python  
import colorama  
iprint(  
    'yang ini',  
    {'12':12,'sdsd':{'12':21,'as':[88]}},  
    color=colorama.Fore.BLUE + colorama.Style.BRIGHT  
)  
```

Output:
```py
[34m[1myang ini[0m [34m[1m{'12': 12, 'sdsd': {'12': 21, 'as': [88]}}[0m
```

## irange

`irange(start, finish, step=1)`

Meningkatkan fungsi range() dari python untuk pengulangan menggunakan huruf  
  
```python  
print(irange('a', 'c'))  
print(irange('z', 'a', 10))  
print(list(irange('a', 'z', 10)))  
print(list(irange(1, '7')))  
print(list(irange(10, 5)))  
```

Output:
```py
<generator object irange at 0x72f4f9aac0>
<generator object irange at 0x72f4f9aac0>
['a', 'k', 'u']
[1, 2, 3, 4, 5, 6, 7]
[10, 9, 8, 7, 6, 5]
```

## ireplace

`ireplace(string: str, replacements: dict, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)`

STRing TRanslate mengubah string menggunakan kamus dari dict.  
Replacement dapat berupa text biasa ataupun regex pattern.  
Apabila replacement berupa regex, gunakan raw string `r"..."`  
Untuk regex capturing gunakan `(...)`, dan untuk mengaksesnya  
gunakan `\1`, `\2`, .., dst.  
  
```python  
text = 'aku ini mau ke sini'  
replacements = {  
    "sini": "situ",  
    r"(ini)": r"itu dan \1",  
}  
print(ireplace(text, replacements))  
```

Output:
```py
aku itu dan ini mau ke situ
```

## iscandir

`iscandir(folder_name='.', glob_pattern='*', recursive=True, scan_file=True, scan_folder=True)`

Mempermudah scandir untuk mengumpulkan folder dan file.  
  
```python  
print(iscandir())  
print(list(iscandir("./", recursive=False, scan_file=False)))  
```

Output:
```py
<generator object iscandir at 0x72f4fd0840>
[PosixPath('.git'), PosixPath('.vscode'), PosixPath('pypipr'), PosixPath('__pycache__'), PosixPath('dist')]
```

## isplit

`isplit(text, separator='', include_separator=False)`

Memecah text menjadi list berdasarkan separator.  
  
```python  
t = '/ini/contoh/path/'  
print(isplit(t, separator='/'))  
```

Output:
```py
['', 'ini', 'contoh', 'path', '']
```

# CLASS

## ComparePerformance

`ComparePerformance()`

Menjalankan seluruh method dalam class,  
Kemudian membandingkan waktu yg diperlukan.  
Nilai 100 berarti yang tercepat.  
  
```python  
class ExampleComparePerformance(ComparePerformance):  
    # number = 1  
    z = 10  
  
    def a(self):  
        return (x for x in range(self.z))  
  
    def b(self):  
        return tuple(x for x in range(self.z))  
  
    def c(self):  
        return [x for x in range(self.z)]  
  
    def d(self):  
        return list(x for x in range(self.z))  
  
pprint.pprint(ExampleComparePerformance().compare_result(), depth=100)  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
```

Output:
```py
{'a': <generator object ExampleComparePerformance.a.<locals>.<genexpr> at 0x72f4fe8520>,
 'b': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
 'c': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 'd': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
{'a': 0, 'b': 0, 'c': 0, 'd': 0}
{'a': 0, 'b': 0, 'c': 0, 'd': 0}
{'a': 0, 'b': 0, 'c': 0, 'd': 0}
{'a': 0, 'b': 0, 'c': 0, 'd': 0}
{'a': 0, 'b': 0, 'c': 0, 'd': 0}
```

## RunParallel

`RunParallel()`

Menjalankan program secara bersamaan.  
  
- `class RunParallel` didesain hanya untuk pemrosesan data saja.  
- Penggunaannya `class RunParallel` dengan cara membuat instance  
  sub class beserta data yg akan diproses, kemudian panggil fungsi  
  yg dipilih `run_asyncio / run_multi_threading / run_multi_processing`,  
  kemudian dapatkan hasilnya.  
- `class RunParallel` tidak didesain untuk menyimpan data, karena  
  setiap module terutama module `multiprocessing` tidak dapat mengakses  
  data kelas dari proses yg berbeda.  
- Semua methods akan dijalankan secara paralel kecuali method dengan  
  nama yg diawali underscore `_`  
- Method untuk multithreading/multiprocessing harus memiliki 2  
  parameter, yaitu: `result: dict` dan `q: queue.Queue`. Parameter  
  `result` digunakan untuk memberikan return value dari method, dan  
  Parameter `q` digunakan untuk mengirim data antar proses.  
- Method untuk asyncio harus menggunakan keyword `async def`, dan  
  untuk perpindahan antar kode menggunakan `await asyncio.sleep(0)`,  
  dan keyword `return` untuk memberikan return value.  
- Return Value berupa dictionary dengan key adalah nama function,  
  dan value adalah return value dari setiap fungsi  
- Menjalankan Multiprocessing harus berada dalam blok  
  `if __name__ == "__main__":` karena area global pada program akan  
  diproses lagi. Terutama pada sistem operasi windows.  
- `run_asyncio()` akan menjalankan kode dalam satu program, hanya  
  saja alur program dapat berpindah-pindah menggunkan  
  `await asyncio.sleep(0)`.  
- `run_multi_threading()` akan menjalankan program dalam satu CPU,  
  hanya saja dalam thread yang berbeda. Walaupun tidak benar-benar  
  berjalan secara bersamaan namun bisa meningkatkan kecepatan  
  penyelesaian program, dan dapat saling mengakses resource antar  
  program.  Akses resource antar program bisa secara langsung maupun  
  menggunakan parameter yang sudah disediakan yaitu `result: dict`  
  dan `q: queue.Queue`.  
- `run_multi_processing()` akan menjalankan program dengan beberapa  
  CPU. Program akan dibuatkan environment sendiri yang terpisah dari  
  program induk. Keuntungannya adalah program dapat benar-benar berjalan  
  bersamaan, namun tidak dapat saling mengakses resource secara langsung.  
  Akses resource menggunakan parameter yang sudah disediakan yaitu  
  `result: dict` dan `q: queue.Queue`.  
  
```py  
class ExampleRunParallel(RunParallel):  
    z = "ini"  
  
    def __init__(self) -> None:  
        self.pop = random.randint(0, 100)  
  
    def _set_property_here(self, v):  
        self.prop = v  
  
    def a(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["a"] = "a"  
        q.put("from a 1")  
        q.put("from a 2")  
  
    def b(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["b"] = "b"  
        result["q_get"] = q.get()  
  
    def c(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["c"] = "c"  
        result["q_get"] = q.get()  
  
    async def d(self):  
        print("hello")  
        await asyncio.sleep(0)  
        print("hello")  
  
        result = {}  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["d"] = "d"  
        return result  
  
    async def e(self):  
        print("world")  
        await asyncio.sleep(0)  
        print("world")  
  
        result = {}  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["e"] = "e"  
        return result  
  
if __name__ == "__main__":  
    print(ExampleRunParallel().run_asyncio())  
    print(ExampleRunParallel().run_multi_threading())  
    print(ExampleRunParallel().run_multi_processing())  
```

## APIMixinView

`APIMixinView()`

APIView adalah class view untuk membuat Website API  
Cara kerjanya adalah dengan menggunakan variabel GET untuk menerima data.  
  
Class ini tidak bisa digunakan sendiri.  
Class ini harus menjadi mixin Class View karena perlu trigger untuk  
memanggil method get().  
  
```py  
class ExampleAPIView(APIMixinView, View):  
    pass  
```

## PintUregQuantity

`PintUregQuantity(value, units=None)`
