class Player1:
    #换道车
    def __init__(self, paras, args):
        self.a_min = args.a1_min
        self.a_max = args.a1_max
        self.type = args.type1
        self.v = args.v1
        self.paras = paras

    def payoff(self, mode, v2, t):
        #换道车的收益函数
        w1 = self.paras[self.type]["w1"]
        w2 = self.paras[self.type]["w2"]
        w3 = self.paras[self.type]["w3"]
        alpha = self.paras[mode]["alpha"]
        beta = self.paras[mode]["beta"]
        gamma = self.paras[mode]["gamma"]
        delta_v = self.v - v2

        #最高速度差收益为100
        if delta_v > 10:
            delta_v = 10

        if mode == "acceleration":  # 加速的收益
            a = (w1 * alpha * t + w2 * beta * t) / (2 * w3 * gamma)  # 最大值的横坐标
            a = min(max(a, self.a_min), self.a_max)
            payoff = w1 * alpha * (delta_v + a * t) + w2 * beta * (self.v + a * t) - w3 * gamma * a ** 2
            return payoff, a
        elif mode == "constant":  # 不变的收益
            payoff = w1 * alpha * delta_v + w2 * beta * self.v
            return payoff, 0
        else:
            raise ValueError("Invalid mode")

class Player2:
    def __init__(self, paras, args):
        self.a_min = args.a2_min
        self.a_max = args.a2_max
        self.type = args.type2
        self.v = args.v2
        self.paras = paras
        self.C = {"acceleration": 0.0, "constant": 0.0, "deceleration": 0.0}

    def payoff(self, mode, v1, a1, t, l):
        w1 = self.paras[self.type]["w1"]
        w2 = self.paras[self.type]["w2"]
        w3 = self.paras[self.type]["w3"]
        alpha = self.paras[mode]["alpha"]
        beta = self.paras[mode]["beta"]
        gamma = self.paras[mode]["gamma"]
        C = self.C[mode]
        delta_v = v1 - self.v

        if delta_v > 10:
            delta_v = 10

        if mode == "acceleration":
            a = (-w1 * alpha * t + w2 * beta * t) / (2 * w3 * gamma)
            a = min(max(a, self.a_min), self.a_max)
            if (v1 - self.v) * t + 0.5 * (a1 - a) * t ** 2 > 1.5 * l or (v1 - self.v) * t + 0.5 * (a1 - a) * t ** 2 < -1.5 * l:
                payoff = w1 * alpha * (delta_v - a * t) + w2 * beta * (self.v + a * t) - w3 * gamma * a ** 2 + C
            else:
                payoff = w1 * alpha * (delta_v - a * t) + w2 * beta * (self.v + a * t) - w3 * gamma * a ** 2 + C / 2
            return payoff, a
        elif mode == "constant":
            a = 0
            if (v1 - self.v) * t + 0.5 * (a1 - a) * t ** 2 > 1.5 * l or (v1 - self.v) * t + 0.5 * (a1 - a) * t ** 2 < -1.5 * l:
                payoff = w1 * alpha * delta_v + w2 * beta * self.v + C
            else:
                payoff = w1 * alpha * delta_v + w2 * beta * self.v + C / 2
            return payoff, 0
        elif mode == "deceleration":
            a = (-w1 * alpha * t + w2 * beta * 0.1 * t) / (2 * w3 * gamma)
            a = min(max(a, self.a_min), 0)
            if (v1 - self.v) * t + 0.5 * (a1 - a) * t ** 2 > 1.5 * l or (v1 - self.v) * t + 0.5 * (a1 - a) * t ** 2 < -1.5 * l:
                payoff = w1 * alpha * (delta_v - a * t) + w2 * beta * (self.v + a * t) - w3 * gamma * a ** 2 + C
            else:
                payoff = w1 * alpha * (delta_v - a * t) + w2 * beta * (self.v + a * t) - w3 * gamma * a ** 2 + C / 2
            return payoff, a
        else:
            raise ValueError("Invalid mode")

    def shrink(self, mode):
        self.C[mode] -= 10


