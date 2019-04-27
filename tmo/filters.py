def art(kind):
    def art_in(s):
        return '%s %s' % (kind, s)
    return art_in
