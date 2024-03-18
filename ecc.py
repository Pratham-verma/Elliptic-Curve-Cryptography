import prettytable


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
        self.allPoints = self.find_all_points_on_curve()
        self.orderE = len(self.allPoints)
        self._h = None
        self.pointG = None
        self._n = None

    def update(self, pointG):
        flag = False
        if self.is_point_on_curve(pointG):
            flag = True
            self._pointG = pointG
            self._n = self.count_numb_of_points_in_cyclic_subgroup()
            self._h = int(self._orderE) / int(self._n)
            table = prettytable.PrettyTable(["orderE # points on curve)", "n (subgroup size)", "cofactor h (orderE/n)"])
            table.add_row([self._orderE, self._n, self._h])
            print(table)
        return flag

    def slow_multiply(self, d):  # only use w/ small cyclic subgroups
        pass

    def fast_multiply(self, d):
        pass

    def is_point_on_curve(self, pointG: Point):
        return (pointG.get_y() * pointG.get_y()) % self._p == \
            (pointG.get_x() * pointG.get_x() * pointG.get_x() + (self._a * pointG.get_x() + self._b)) % self._p

    def is_inverse(self, pointG, pointT):
        return self._p == (pointT.get_y() + pointG.get_y()) and pointG.get_x() == pointT.get_x()

    def find_all_points_on_curve(self):
        pointsTable = prettytable.PrettyTable("")
        allPoints = [];
        leftSideCalculation = [];
        rightSideCalculation = []
        i = 0
        while i < self._p:
            rightSideCalculation.append((i * i * i + self._a * i + self._b) % self._p)
            leftSideCalculation.append(i * i % self._p)
            i = i + 1
        i = 0
        while i < self._p:
            j = 0
            points = []
            while j < self._p:
                if rightSideCalculation[i] == leftSideCalculation[j]: points.append(Point(i, j))
                j = j + 1
            allPoints.extend(points)
            if len(points) > 0: pointsTable.add_row([str(points)])
            i = i + 1
            allPoints.extend(points)
            if len(points) > 0: pointsTable.add_row([str(points)])
            i = i + 1
        allPoints.append(EllipticCurve.POINT_AT_INFINITY)
        pointsTable.add_row([str(EllipticCurve.POINT_AT_INFINITY)])
        self.display_points_matching_table(leftSideCalculation, rightSideCalculation)
        self.display_all_points_on_curve(allPoints, pointsTable)
        return allPoints

    def count_numb_of_points_in_cyclic_subgroup(self):
        pass

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
                if entry.lower() == "e":
                    break
                elif ' ' in entry:
                    a, b, p = map(int, entry.split(' '))

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
        if flag:
            exit()
        return ec

    def handle_generator_point_input(self, ec: EllipticCurve):
        flag = True
        while True:
            entry = input("> Please enter Generator Point x & y coordinates, or e:exit\n")
            if entry.lower() == "e":
                flag = False
                break
            else:
                if ' ' not in entry:
                    print("Invalid input: Please provide both x and y coordinates separated by a space.")
                    continue
                x, y = entry.split(' ')
                try:

                    pointG = Point(x, y)
                    if not ec.update(pointG):
                        print("Point is not on the curve.")
                    else:
                        break
                except ValueError:
                    print("Invalid input: Please enter valid numeric coordinates.")

        return flag

    def handle_point_hopping_input(self, type, ec: EllipticCurve):
        pass


Driver.run_app()
