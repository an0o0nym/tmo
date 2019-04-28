def art(kind):
    def art_in(s):
        return '%s %s' % (kind, s)
    return art_in


def join(connector_word=None, separator_char=None):
    """
    :param connector_word: a CHARACTER joining all elements of
           multi-value argument, except last two elements.
    :param separator_char: a WORD joining last two elements of
           multi-value argument.
    """
    connector_word = connector_word or ' and '
    separator_char = separator_char or ', '

    def join_in(val):
        v_head, v_tail = val[:-2], val[-2:]
        v_tail = [connector_word.join(v_tail)]
        return separator_char.join(v_head + v_tail)
    return join_in
