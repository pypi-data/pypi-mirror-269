from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Tuple

from tp_interfaces.abstract import AbstractDocumentProcessor


def _named_path(arg: str) -> Tuple[str, Path]:
    if ":" not in arg:
        return "", Path(arg)
    name, path = arg.split(":", 1)
    return name, Path(path)


def get_processor_factory(parser: ArgumentParser):
    argument_group = parser.add_argument_group(title='Model arguments')
    argument_group.add_argument('-m', '--model_paths', action='append', type=_named_path, metavar='<model name:model path>', required=True,
                                help='Named paths to configuration files or serialized models')
    argument_group.add_argument('--wrapper', type=Path, metavar='<wrapper path>', help='Path to wrapper configuration file', default=None)
    argument_group.add_argument('--omit_merging', action='store_true', help='Disable model merging during configuration')

    def get_processor(args: Namespace) -> AbstractDocumentProcessor:
        from talisman_tools.configure import load_or_configure, wrap_model
        from talisman_tools.configure.configure import read_config

        processor = load_or_configure(model_or_config_named_paths=args.model_paths, merge=not args.omit_merging)
        if args.wrapper is not None:
            processor = wrap_model(processor, read_config(args.wrapper), merge=not args.omit_merging)
        return processor

    return get_processor
