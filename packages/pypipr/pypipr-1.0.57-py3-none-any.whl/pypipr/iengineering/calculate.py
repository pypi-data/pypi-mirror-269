from .PintUregQuantity import PintUregQuantity


def calculate(teks):
    """
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
    """
    return PintUregQuantity(teks)


if __name__ == "__main__":
    from ..ifunctions.iargv import iargv

    if i := iargv(1):
        print(i)
