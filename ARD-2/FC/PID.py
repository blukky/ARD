

class PID_controller:

    def __init__(self, params, limit):
        self.params = params # {k_p, k_i, k_d}
        self.limit = limit #{min, max}
        self.integral = 0
        self.last_error = 0
        self.e = 0

    def PID(self, target,  pose,  dt):
        self.e = target - pose
        self.integral += self.e * dt
        u = self.params.get("k_p", 0.5) * self.e + \
            self.integral * self.params.get("k_i", 0.1) + \
            self.params.get("k_d", 0.1) * ((self.e - self.last_error) / dt)
        self.last_error = self.e
        u = max(self.limit.get("min"), min(u, self.limit.get("min")))
        return u
