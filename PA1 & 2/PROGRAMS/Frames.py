from numpy import linalg
#The Frame Library.
#Methods: 
#   __init__    (Create a frame)
#       Inputs:
#           R:      3x3 rotation matrix 
#           p:      3x1 translation vector

#   getR        (get a frame's rotation matrix)
#       Outputs:
#           3x3 rotation matrix R

#   getp        (get a frame's translation vector)
#       Outputs:
#           3x1 translation vector t

#   getInverse  (get the inverted version of a frame)
#       Inputs:
#           self:    Frame object to invert
#       Outputs:
#           New Frame object defined as F = (R^-1, -R^-1 * p)

#----------------------------------------------------

#Frame Composition Methods:

#   compose_frames  (F1 * F2)
#       Inputs:
#           F1:     Frame object 1
#           F2:     Frame object 2
#       Outputs:
#           new Frame object defined as F1*F2 = (R1R2, R1p2 + p1)

#   frame_times_vector  (F*v)
#       Inputs:
#           F:      Frame object (R,p)
#           v:      3x1 vector
#       Outputs:
#           3x1 vector defined as a = R*v + p

class Frame:
    def __init__(self, R, p):
        if R.shape != (3,3):
            raise Exception(f"matrix A is not 3x3")
        if (abs(linalg.det(R)) - 1 > .0001):
            print(linalg.det(R))
            raise Exception(f"matrix A is not a rotation")
        if p.shape != (3,):
            raise Exception(f"p is not 3x1")

        self.R = R
        self.p = p

    def getR(self):
        return self.R
    
    def getp(self):
        return self.p

    def getInverse(self):
        return Frame(linalg.inv(self.R), (-linalg.inv(self.R) @ self.p.reshape(3,1)).reshape(3,))


def compose_frames(A, B):
    return Frame(A.getR() @ B.getR(), (A.getR() @ B.getp().reshape(3, 1) + A.getp().reshape(3, 1)).reshape(3,))


def frame_times_vector(F, v):
    return (F.getR() @ v + F.getp()).reshape(3,)
