class RunningMean(dict):

    def __init__(self, new_obs_weight, state_init="first", **kwargs):
        """
        Apply running mean on streaming data. New running mean is computed
        like:
        new_state = old_state * (1 - new_obs_weight) + obs * new_obs_weight

        :param new_obs_weight: weight given to new obs
        :param state_init: way to initialize the state. Can be numeric or
            the string "first" in which case the first obs is used.
        """
        super(RunningMean, self).__init__(**kwargs)
        self['new_obs_weight'] = new_obs_weight
        self['state'] = state_init

    def observe(self, obs):
        """
        Update running mean with new observation

        :param obs: observation
        :return: the new running mean
        """
        # convert to float and test if obs can be interpreted as numeric at
        # the same time
        obs = float(obs)

        if self['state'] == "first":
            self['state'] = obs

        self['state'] = RunningMean.running_mean(self['state'], obs,
                                              self['new_obs_weight'])
        return self['state']

    def __repr__(self):
        return "RunningMean(new_obs_weight=%f,state=%s)" % \
               (self['new_obs_weight'], str(self['state']))

    @staticmethod
    def from_dict(d):
        if 'new_obs_weight' not in d:
            raise ValueError('new_obs_weight not specified in dict')
        if 'state' not in d:
            raise ValueError('state not specified in dict')
        return RunningMean(d['new_obs_weight'], d['state'])

    @staticmethod
    def running_mean(state, obs, weight):
        """
        New state of a running mean given observation and weight

        :param state: old state
        :param obs: new observation
        :param weight: weight of observation
        :return: new state
        """
        return state * (1.0 - weight) + obs * weight

    @staticmethod
    def series_running_mean(series, new_obs_weight, init = "first"):
        """
        Apply running mean on a the numeric pandas Series.

        In comparison to the pandas .rolling functions this has a state
        while the pandas function have a window.

        :param series: a pandas Series
        :param new_obs_weight: weight given to new obs
        :return: filtered series
        """
        state = init
        if state == "first":
            state = series.reset_index(drop=True).loc[0]

        states = []
        for i in series:
            state = RunningMean.running_mean(state, i, new_obs_weight)
            states.append(state)
        series[:] = states

        return series


if __name__ == "__main__":
    from pandas import Series
    a = Series([1, 10, 100, 1000])
    b = RunningMean.series_running_mean(a, .5)
    print(b)
    # should be: Series([1, 5.5, 52.75, 526.375])
    state = RunningMean(.5)
    states = []
    for i in a:
        state.observe(i)
        states.append(i)
    print(states)
    # should be [1, 5.5, 52.75, 526.375]
