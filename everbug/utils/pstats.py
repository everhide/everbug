from pstats import Stats
from pstats import func_std_string as fss


class StatsDict(Stats):

    def dump(self, short=False):
        """ lines is a list of tuples: (ncalls, tottime, cumtime, func) """
        fns = self.fcn_list
        if not fns:
            return None
        prof = {
            'total_calls': self.total_calls,
            'total_time': round(self.total_tt, 3),
            'lines': []
        }
        if short:
            fns, *_ = self.eval_print_amount(20, self.fcn_list, '')
        for f in fns:
            cc, nc, tt, ct, callers = self.stats[f]
            nc = nc if nc == cc else '%s/%s' % (nc, cc)
            prof['lines'].append((nc, round(tt, 3), round(ct, 3), fss(f)))
        return prof
