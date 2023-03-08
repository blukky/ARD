

class PID_controller:

    def __init__(self, params):
        self.params = params # {k_p, k_i, k_d, max, min}
        self.integral = 0
        self.last_error = 0
        self.e = 0

    def PID(self, target,  pose,  dt):
        self.e = target - pose
        self.integral += self.params.get("k_i") * (self.e + self.last_error) * dt / 2
        self.integral = max(self.params.get("min"), min(self.integral, self.params.get("max")))
        u = self.params.get("k_p") * self.e + \
            self.integral + \
            self.params.get("k_d") * ((self.e - self.last_error) / dt)
        self.last_error = self.e
        u = max(self.params.get("min"), min(u, self.params.get("max")))
        return u


    def __str__ (self):
        return f"PID: {self.params}"
