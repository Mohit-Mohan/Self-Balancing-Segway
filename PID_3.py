class PID:
    # Calculate the pitch error pError
    # Compute the output as sum of P, I and D terms
    # Accumulate the pError term for integration
    # Limit the output W to +-100
    # Return the W drive value
    
    
    def PID(error, error_int, rate_pitch):
        kp = 20.3
        ki = 17.8
        kd = 42

        P = kp * error
        I = ki * error_int
        D = kd * rate_pitch

        PID = P + I + D
        speed = max(min(PID, 100), -100)
        return speed



