#!/usr/bin/env python3
import kconfiglib
import sys


def main() -> None:
    kconf = kconfiglib.Kconfig(sys.argv[1])

    boolean_count = 0
    tristate_count = 0
    switch_count = 0
    int_count = 0
    ranges_count = 0
    str_count = 0
    hex_count = 0
    mutex_count = 0
    or_count = 0
    xor_count = 0
    unknown_count = 0

    with open("/tmp/numeric_features_linux.txt", 'w') as output_file:
        with open("/tmp/unknown_options.txt", 'w') as unknown_options_file:
            with open("/tmp/known_options.txt", 'w') as known_options_file:
                for symbol_name in kconf.syms.keys():
                    symbol: kconfiglib.Symbol = kconf.syms[symbol_name]
                    if symbol.orig_type != kconfiglib.UNKNOWN:
                        known_options_file.write(f"{symbol.name_and_loc}\n\n")
                    match symbol.orig_type:
                        case kconfiglib.BOOL:
                            boolean_count += 1
                            switch_count += 1
                        case kconfiglib.TRISTATE:
                            tristate_count += 1
                            switch_count += 1
                        case kconfiglib.INT:
                            int_count += 1
                            if len(symbol.ranges) > 0:
                                ranges_count += 1
                                output_file.write(f"[{ranges_count}. {symbol_name}]\n")
                                output_file.write(f"Range: {symbol.ranges}\n")
                                output_file.write(f"{symbol.nodes[0].help}\n\n")
                        case kconfiglib.STRING:
                            str_count += 1
                        case kconfiglib.HEX:
                            hex_count += 1
                        case kconfiglib.UNKNOWN:
                            unknown_count += 1
                            unknown_options_file.write(f"[{symbol_name}]\n")
                            unknown_options_file.write(f"{symbol.type}\n")
                            unknown_options_file.write(f"{symbol.name_and_loc}\n\n")

        for choice in kconf.choices:
            if choice.is_optional and choice.orig_type == kconfiglib.BOOL:
                mutex_count += 1
            elif not choice.is_optional and choice.orig_type == kconfiglib.TRISTATE:
                or_count += 1
            elif not choice.is_optional and choice.orig_type == kconfiglib.BOOL:
                xor_count += 1
            else:
                print(choice.name)
                print(choice.name_and_loc)

    print(f"Mutex: {mutex_count} ({mutex_count / (1.0 * len(kconf.choices)) * 100}%)")
    print(f"Or: {or_count} ({or_count / (1.0 * len(kconf.choices)) * 100}%)")
    print(f"Xor: {xor_count} ({xor_count / (1.0 * len(kconf.choices)) * 100}%)")
    print(f"Boolean options: {boolean_count}/{len(kconf.syms)} ({boolean_count / (1.0 * len(kconf.syms)) * 100}%)")
    print(f"Tristate options: {tristate_count}/{len(kconf.syms)} ({tristate_count / (1.0 * len(kconf.syms)) * 100}%)")
    print(f"Switch options: {switch_count}/{len(kconf.syms)} ({switch_count / (1.0 * len(kconf.syms)) * 100}%)")
    print(f"Numeric options: {int_count}/{len(kconf.syms)} ({int_count / (1.0 * len(kconf.syms)) * 100}%)")
    print(f"Numeric options with ranges: {ranges_count}/{len(kconf.syms)} ({ranges_count / (1.0 * len(kconf.syms)) * 100}%)")
    print(f"String options: {str_count}/{len(kconf.syms)} ({str_count / (1.0 * len(kconf.syms)) * 100}%)")
    print(f"Hex options: {hex_count}/{len(kconf.syms)} ({hex_count / (1.0 * len(kconf.syms)) * 100}%)")
    print(f"Unknown options: {unknown_count}/{len(kconf.syms)} ({unknown_count / (1.0 * len(kconf.syms)) * 100}%)")


if __name__ == "__main__":
    main()
