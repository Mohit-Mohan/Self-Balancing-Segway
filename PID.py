class PIDC:
    def __init__(self, kp, kd, ki, theta_0):
        self.kp = kp
        self.kd = kd
        self.ki = ki

        self.baseTarget = theta_0 
        self.target = theta_0
        self.limit = 2
        self.integrator = 0

    def target_reset(self):
        self.target = self.baseTarget
        self.integrator = 0

    def get_pwm(self, pitch, pitch_dot):
        pError = self.target - pitch

        output = self.kp * pError + self.kd * pitch_dot + self.ki *self.integrator

        self.integrator += pError

        if output > 100:
            output = 100
        elif output < -100:
            output = -100
        return output
