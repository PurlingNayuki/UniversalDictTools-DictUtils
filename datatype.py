class Dictionary:
    _entries = []
    def __init__(self, name, * entries):
        self.name = name
        if len(entries) > 0:
            for entry in entries:
                if isinstance(entry, Entry):
                    self._entries.append(entry)

    def __len__(self):
        return len(self._entries)

    def __getitem__(self, item):
        return self.lookup(item)

    def has(self, hw: str):
        for entry in self._entries:
            if entry.name == hw:
                return True
        return False

    def append(self, entry):
        assert isinstance(entry, Entry)
        self._entries.append(entry)

    def lookup(self, hw):
        result = []
        for entry in self._entries:
            if entry.name == hw:
                result.append(entry)

        if len(result) > 0:
            return result
        else:
            return None

    def to_dict_name(self):
        result = dict()
        for entry in self._entries:
            if entry.name in result:
                result[entry.name].append(entry)
            else:
                result[entry.name] = [entry]

        return result

    def to_dict_id(self):
        result = dict()
        for entry in self._entries:
            if entry.id in result:
                result[entry.id].append(entry)
            else:
                result[entry.id] = [entry]

        return result

class Entry:
    def __init__(self, hw: str, *, content = '', hwid = '', title=''):
        self.name = hw
        self.content = content
        self.id = hwid
        self.title = title