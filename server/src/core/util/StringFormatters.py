class StringFormatters:

  @staticmethod
  def convert_dict_keys_to_comma_seperated_list(dictionary: dict):
    return ",".join(list(dictionary.keys()))