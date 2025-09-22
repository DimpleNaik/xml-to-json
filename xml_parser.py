import re

def replace_entities(text):
    # Replace standard XML entities
    entities = {
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&quot;": "\"",
        "&apos;": "'"
    }
    for k, v in entities.items():
        text = text.replace(k, v)
    return text

def remove_declaration_and_comments(xml):
    # Remove XML declaration
    xml = re.sub(r'<\?xml.*?\?>', '', xml)
    # Remove comments
    xml = re.sub(r'<!--.*?-->', '', xml, flags=re.DOTALL)
    return xml.strip()

def parse_attributes(attr_string):
    # Parse tag attributes into dict
    attrs = {}
    attr_pattern = re.compile(r'(\w+)\s*=\s*"([^"]*)"')
    for match in attr_pattern.finditer(attr_string):
        key, val = match.groups()
        attrs[key] = replace_entities(val)
    return attrs

def tokenize(xml):
    # Tokenize XML into tags and text
    tokens = []
    tag_regex = re.compile(r'(<[^>]+>)')
    pos = 0
    for m in tag_regex.finditer(xml):
        if m.start() > pos:
            # Text before the tag
            text = xml[pos:m.start()].strip()
            if text:
                tokens.append(('text', replace_entities(text)))
        tokens.append(('tag', m.group(1)))
        pos = m.end()
    if pos < len(xml):
        text = xml[pos:].strip()
        if text:
            tokens.append(('text', replace_entities(text)))
    return tokens

def parse(tokens):
    # Recursive parser using tokens and stack behavior
    def parse_node(idx):
        result = {}
        text_content = []

        while idx < len(tokens):
            ttype, val = tokens[idx]

            if ttype == 'text':
                text_content.append(val)
                idx += 1
                continue

            tag_content = val[1:-1].strip()

            # Closing tag
            if tag_content.startswith('/'):
                if text_content:
                    # Return text directly if it's the only thing
                    return " ".join(text_content), idx + 1
                return result, idx + 1

            # Self-closing tag
            elif tag_content.endswith('/'):
                space_pos = tag_content.find(' ')
                if space_pos == -1:
                    tag_name = tag_content[:-1].strip()
                    attrs = {}
                else:
                    tag_name = tag_content[:space_pos].strip()
                    attrs_str = tag_content[space_pos:-1].strip()
                    attrs = parse_attributes(attrs_str)

                element = {}
                if attrs:
                    element["@attributes"] = attrs

                if tag_name in result:
                    if isinstance(result[tag_name], list):
                        result[tag_name].append(element)
                    else:
                        result[tag_name] = [result[tag_name], element]
                else:
                    result[tag_name] = element

                idx += 1
                continue

            # Opening tag
            else:
                parts = tag_content.split(None, 1)
                tag_name = parts[0]
                attrs = {}
                if len(parts) == 2:
                    attrs = parse_attributes(parts[1])

                idx += 1
                children, idx = parse_node(idx)

                # If children is just text, keep as string
                element = children
                if isinstance(children, dict) and not children:
                    element = ""
                if isinstance(children, dict):
                    element = children

                if attrs:
                    if isinstance(element, dict):
                        element["@attributes"] = attrs
                    else:
                        element = {"@attributes": attrs, "#text": element}

                if tag_name in result:
                    if isinstance(result[tag_name], list):
                        result[tag_name].append(element)
                    else:
                        result[tag_name] = [result[tag_name], element]
                else:
                    result[tag_name] = element

        if text_content:
            return " ".join(text_content), idx
        return result, idx

    parsed_result, _ = parse_node(0)
    return parsed_result

def xml_to_json(xml_string):
    xml_string = remove_declaration_and_comments(xml_string)
    tokens = tokenize(xml_string)
    parsed = parse(tokens)
    return parsed
