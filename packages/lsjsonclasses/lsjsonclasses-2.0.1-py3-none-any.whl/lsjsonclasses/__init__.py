import datetime
import json
from typing import Union

import iso8601 as iso8601
from iso8601 import ParseError


class LSoftJSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, (datetime.date, datetime.datetime)):
			return obj.isoformat()

	@classmethod
	def dumps(cls, obj, *args, **kwargs):
		return json.dumps(obj, *args, cls=cls, **kwargs)


def str_to_datetime_if_parseable(value: str) -> Union[datetime.datetime, str]:
	if len(value) < 8 or value.count('-') != 2:
		return value
	try:
		ret = iso8601.parse_date(value)
	except (ParseError, ValueError, TypeError):
		ret = value
	return ret


class LSoftJSONDecoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		super().__init__(object_hook=self.try_datetime, *args, **kwargs)

	@staticmethod
	def try_datetime(d):
		ret = {}
		for key, value in d.items():
			if isinstance(value, str):
				ret[key] = str_to_datetime_if_parseable(value)
			else:
				ret[key] = value
		return ret

	@classmethod
	def loads(cls, s, *args, **kwargs):
		return json.loads(s, *args, cls=cls, **kwargs)


def import_json(file_path: str) -> dict:
	with open(file_path, "r", encoding='utf8') as fd:
		data = json.load(fd, cls=LSoftJSONDecoder)
	return data
