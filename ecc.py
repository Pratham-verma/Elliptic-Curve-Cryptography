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
        hopsTable = prettytable.PrettyTable()
        hopsTable.header = False
        hops = [];
        hop = []
        i = 1
        pointT = EllipticCurve.POINT_AT_INFINITY
        while (i <= d):
            if not self.is_inverse(self._pointg, pointT):
                if self.pointG == pointT:
                    pointT = self.double(self._pointG)
                else:
                    pointT = self.add(self._pointG, pointT)
                hop.append(str(i) + str(self._pointG) + "=" + str(pointT))
            else:
                pointT = EllipticCurve.POINT_AT_INFINITY
                hop.append(str(i) + str(self._pointG) + "=" + str(pointT))
                hops.append(hop)
                hop = []
            if i == d: hops.append(hop)
            i = i + 1
            self.add_rows_to_table(d, hopsTable, hops)
            print(hopsTable)
            self.display_result(d, self._pointG, pointT)
            return pointT

    def fast_multiply(self, d):
        table = prettytable.PrettyTable(["step#", "bit", "double", "& add (bit = 1)"])
        baseChangeStr = ""
        pointT = EllipticCurve.POINT_AT_INFINITY
        if d < self._n:
            dInBinary = str(bin(d).replace("0b" , ""))
            baseChangeStr = baseChangeStr + str(d) + "|Base10 = " + dInBinary + "|Base2"
            table.add_row(["[0]", "1", "[0G + 0G = 0G]", "[0G + 1G = 1G]"])
            pointT = Point(self.pointG.get_x(), self._pointG.get_y())
            q = 1;
            p = 1
            for i in range(1, len(dInBinary)):
                bit = int(dInBinary[i])
                row = [str(i), str(bit)]
                rowContent = str(q) + "G+" + str(q) + "G="
                q = q + q
                rowContent = rowContent + str(q) + "G"
                row.append(rowContent)
                pointT = self.double(pointT)
                if bit == 1:
                    rowContent = " " + str(q) + "G+" + str(p) + "G="
                    q = q + p
                    rowContent = rowContent + str(q) + "G"
                    row.append(rowContent)
                    pointT = self.add(self._pointG, pointT)
                else:
                    row.append("")
                table.add_row(row)
            print(baseChangeStr)
            print(table)
            self.display_result(d, self._pointG, pointT)
            return pointT

    def add(self, pointG, pointQ):
        if pointG == pointQ:
            returnValue = self.double(pointG)
        elif pointG == EllipticCurve.POINT_AT_INFINITY:
            returnValue = pointQ
        elif pointQ == EllipticCurve.POINT_AT_INFINITY:
            returnValue = pointG
        else:
            s = ((pointQ.get_y() - pointG.get_y()) % self._p) * (
                self.mod_inverse(pointQ.get_x() - pointG.get_x(), self._p))
            Rx = (s * s - pointG.get_x() - pointQ.get_x()) % self._p
            Ry = (s * (pointG.get_x() - Rx) - pointG.get_y()) % self._p
            returnValue = Point(Rx, Ry)
            return returnValue

    def double(self, pointG):
        if self._pointG == EllipticCurve.POINT_AT_INFINITY:
            returnValue = self.pointG
        else:
            s = (3 * pow(pointG.get_x(), 2, self._p) + self._a) % self._p * \
                self.mod_inverse(2 * pointG.get_y(), self._p)
            Rx = (s * s - pointG.get_x() - pointG.get_x()) % self._p
            Ry = (s * (pointG.get_x() - Rx) - pointG.get_y()) % self._p
            returnValue = Point(Rx, Ry)
            return returnValue

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
        n = 1
        pointT = EllipticCurve.POINT_AT_INFINITY
        while n < self._orderE:
            if not self.is_inverse(self._pointG, pointT):
                if self.pointG == pointT:
                    pointT = self.double(self._pointG)
                else:
                    pointT = self.add(self._pointG, pointT)
            else:
                break
            n = n + 1
        return n


    def get_n(self):
        return self._n

    def mod_inverse(self, c, p):
        inverse = -1
        for numb in range(1, p):
            if ((c % p) * (numb % p)) % p == 1:
                inverse = numb
                break
        return inverse

    @staticmethod
    def is_non_singular(a, b):
        return not (-16) * (4 * a * a * a + 27 * b + b) == 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "y^2 <congruent> x^3 + " + str(self._a) + "x + " + str(self._b) + " mod " + str(self._p)


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
        while True:
            try:
                d = int(input("> please enter # of point hops d\n"))
                if type == "slow":
                    ec.slow_multiply(d)
                    break
                elif type == "fast":
                    if d == ec.get_n():
                        ec.fast_multiply(d)
                        break
                    else:
                        print("# of Point hops d must be <= " + str(
                            ec.get_n()) + " (i.e. n, the # of points in cyclic subgroup)")
            except:
                print("invalid input. ")


Driver.run_app()
