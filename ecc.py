class Point():
    def __init__(self, x, y):
        self._x = int(x)
        self._y = int(y)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        returnValue = "0"

        if self._y != EllipticCurve.INFINITY:
            returnValue = "(" + str(self._x) + "," + str(self._y) + ")"
            return returnValue

    def __eq__(self, o: object):
        returnFlag = False
        if isinstance(o, Point):
            if o._x == self._x and o._y == self._y: returnFlag = True
        return returnFlag

    def __hash__(self):
        return hash(self._x, self._y)


class EllipticCurve():
    INFINITY = int("9999999999999999999999999999999999999999999999999999999999999999999999")
    POINT_AT_INFINITY = Point(0, INFINITY)

    def __init__(self, a, b, p):
        self._a = int(a)
        self._b = int(b)
        self._p = int(p)

    def is_point_on_curve(self, pointG: Point):
        return (pointG.get_y() * pointG.get_y()) % self._p == \
            (pointG.get_x() * pointG.get_x() * pointG.get_x() + (self._a * pointG.get_x() + self._b)) % self._p

    @staticmethod
    def is_non_singular(a, b):
        return not (-16) * (4 * a * a * a + 27 * b + b) == 0


class Driver():
    def run_app(self):

        ec = self.handle_elliptic_curve_input()
        while True:
            entry = input("> what do you want to do? (s:low hops, f:ast hops w/ double & add, c:hange curve, e:xit)\n")

            if entry == "s":
                self.handle_point_hopping_input("slow", ec)
            elif entry == "f":
                self.handle_point_hopping_input("fast", ec)
            elif entry == "c":
                break
            elif entry == "e":
                exit()
            else:
                print("invalid input.")

    def handle_elliptic_curve_input(self):
        ec = None
        flag = False
        while True:
            try:
                entry = input("> please enter a, b, & p (E: y^2 <congruent> x^3 + ax + b mod p), or e:xit\n")
                if ' ' in entry:
                  a, b, p = entry.split(' ')
                else entry == "e":
                    if EllipticCurve.is_non_singular(int(a), int(b)):
                        ec = EllipticCurve(a, b, p)
                    else:
                        print("invalid entry:  singular elliptic curve")
                        continue
                    while True:
                        try:
                            if not self.handle_generator_point_input(ec):
                                flag = True
                                break
                            else:
                                break
                        except:
                             print("invalid input.")
                    break
            except:
                print("invalid input(usage : a b p where E: y^2 <congruent> x^3 + ax + b mod p)")
        if flag: exit()
        return ec
    def handle_generator_point_input(self, ec: EllipticCurve):
        pass

    def handle_point_hopping_input(self, type, ec: EllipticCurve):
        pass


Driver.run_app()
