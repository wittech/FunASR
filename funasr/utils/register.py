import logging
import inspect
from dataclasses import dataclass, fields


@dataclass
class ClassRegistryTables:
    model_classes = {}
    frontend_classes = {}
    specaug_classes = {}
    normalize_classes = {}
    encoder_classes = {}
    decoder_classes = {}
    joint_network_classes = {}
    predictor_classes = {}
    stride_conv_classes = {}
    tokenizer_classes = {}
    batch_sampler_classes = {}
    dataset_classes = {}
    index_ds_classes = {}

    def print_register_tables(self,):
        print("\nregister_tables: \n")
        fields = vars(self)
        for classes_key, classes_dict in fields.items():
            print(f"-----------    ** {classes_key.replace('_meta', '')} **    --------------")
        
            if classes_key.endswith("_meta"):
                headers = ["class name", "register name", "class location"]
                metas = []
                for register_key, meta in classes_dict.items():
                    metas.append(meta)
                metas.sort(key=lambda x: x[0])
                data = [headers] + metas
                col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]
            
                for row in data:
                    print("| " + " | ".join(str(item).ljust(width) for item, width in zip(row, col_widths)) + " |")
        print("\n")

registry_tables = ClassRegistryTables()

def register_class(registry_tables_key:str, key=None):
    def decorator(target_class):
        
        if not hasattr(registry_tables, registry_tables_key):
            setattr(registry_tables, registry_tables_key, {})
            logging.info("new registry table has been added: {}".format(registry_tables_key))

        registry = getattr(registry_tables, registry_tables_key)
        registry_key = key if key is not None else target_class.__name__
        registry_key = registry_key.lower()
        # import pdb; pdb.set_trace()
        assert not registry_key in registry, "(key: {} / class: {}) has been registered already，in {}".format(registry_key, target_class, registry_tables_key)

        registry[registry_key] = target_class
        
        # meta， headers = ["class name", "register name", "class location"]
        registry_tables_key_meta = registry_tables_key + "_meta"
        if not hasattr(registry_tables, registry_tables_key_meta):
            setattr(registry_tables, registry_tables_key_meta, {})
        registry_meta = getattr(registry_tables, registry_tables_key_meta)
        class_file = inspect.getfile(target_class)
        class_line = inspect.getsourcelines(target_class)[1]
        meata_data = [f"{target_class.__name__}", f"{registry_key}", f"{class_file}:{class_line}"]
        registry_meta[registry_key] = meata_data
        # print(f"Registering class: {class_file}:{class_line} - {target_class.__name__} as {registry_key}")
        return target_class
    return decorator

import funasr

