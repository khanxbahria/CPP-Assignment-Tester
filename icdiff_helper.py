from icdiff import *

def custom_diff(yourf, expectedf, view_whole=False):
    custom_args = (f"{yourf} {expectedf} -N -L Your-Output -L"
                    f"Expected-Output").split()
    if view_whole:
        custom_args.append('-W')
    diffs_found = False
    parser = create_option_parser()
    options, args = parser.parse_args(custom_args)
    validate_has_two_arguments(parser, args)
    if not options.cols:
        set_cols_option(options)
    try:
        diffs_found = diff(options, *args)
    except KeyboardInterrupt:
        pass
    except IOError as e:
        if e.errno == errno.EPIPE:
            pass
        else:
            raise


