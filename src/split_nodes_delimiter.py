from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            node_list.append(node)
        else:
            parts = node.text.split(delimiter)

            if len(parts) == 1:
                node_list.append(node)
                continue
            elif len(parts) % 2 == 0:
                raise Exception(f"for node: {node} unmatched delimiter: {delimiter}")

            for i in range(len(parts)):
                if parts[i] == "":
                    continue
                elif i % 2 == 0:
                    node_list.append(TextNode(parts[i], TextType.TEXT))
                else:
                    node_list.append(TextNode(parts[i], text_type))
    return node_list