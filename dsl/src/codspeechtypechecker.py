import copy

import sys
sys.path.insert(0,"../..")

class TypeChecker:
  def __init__(self):
    self.env = [{}]
    self.error = 0

#---------------------------------------------------------------------
# Self.Environment
#---------------------------------------------------------------------
  
  # Close scope
  def _pop(self):
    self.env.pop()

  # Open new scope
  def _put(self):
    return self.env.append(copy.copy(self.env[-1]))

  # Add (Iden,Type) to the self.environment
  def _add(self,ident,type):
    if self._varExist(ident[1]):
      print "%s REFERENCE SELF.ERROR[variable already exists]: %s" \
          % (ident[2],ident[1])
      self.error = 1
    else:
      self.env[-1][ident[1]] = type

      # Return the type of an Ident
  def _type(self,ident):
    try:
      if ident[0] == 'IDENT':
        return self.env[-1][ident[1]]
      elif ident[0] == 'THIS':
        return self.env[-1][ident[1]][ident[2][1]]
      elif ident[0] == 'OTHER':
        return self._typeParams(self.env[-1][ident[1][1]][ident[2]],ident[3][1])
      elif ident[0] == 'COMP':
        return self._typeParams(self.env[-1][ident[1][0][1]][ident[2]],ident[3][1])

    except KeySelf.Error:
      print "%s REFERENCE SELF.ERROR[variable not found]: %s" \
          % (ident[-1][2],self.showArg(ident))
      self.error = 1

  # Returns type of a parameter 'p' from a list of parameters
  def _typeParams(self,params,p):
    for x in params:
      if x[1][1] == p: return x[0]

  # Returns if variable exists in self.environment
  def _varExist(self,var):
    return self.env[-1].has_key(var)

  # Add parameter to input/output record
  def _addParam(self,io,param):
    if self.env[-1][io].has_key(param[1][1]):
      print "%s REFERENCE SELF.ERROR[variable already exists]: %s" \
          % (param[1][2],param[1][1])
      self.error = 1
    elif param[2] == 'DEFAULT' and param[0] != param[3][0].title():
      print "%s TYPE SELF.ERROR[default value]: %s:%s, %s:%s" \
          % (param[1][2],param[1][1],param[0]          \
            ,param[3][1],param[3][0].title())
    else:
      self.env[-1][io][param[1][1]] = param[0]

#---------------------------------------------------------------------
# Type Check
#---------------------------------------------------------------------

  def _checkCompStmt(self,c):
    args = copy.copy(self._type(c[0])['in'])
    if self.error == 0:
      for x in c[1]:
        if args == []:
          print "%s REFERENCE SELF.ERROR[input out of bounds]: %s" \
              % (x[-1][2],self.showArg(x))
          self.error = 1
        else:
          y = args.pop(0)
          tx = self.typecheck(x)
          if tx != y[0] and self.error == 0:
            print "%s TYPE SELF.ERROR[assignment]: %s:%s, %s:%s" \
                % (x[-1][2],self.showArg(x)              ,tx   \
                  ,self.showArg(['OTHER',c[0],'in',y[1]]),y[0])
            self.error = 1

  def typecheck(self,t):
    # Nothing to check
    if t == []:
      pass

    # Program: check import, components
    elif t[0] == 'PROGRAM':
      map(self.typecheck,t[2])
      ctx = copy.copy(self.env[-1])
      self.env = [{}]
      if self.error == 0: return ctx

    # Network: check controller, network block
    elif t[0] == 'NETWORK':
      self.typecheck(t[1])
      map(self.typecheck,t[2])

    # Component: check paramaters, network/atom
    elif t[0] == 'COMPONENT':
      self._add(t[1],{'in':t[3],'out':t[4]})
      self._put()
      self._add(['IDENT','in'],{})
      self._add(['IDENT','out'],{})
      map(lambda x:self._addParam('in',x),t[3])
      map(lambda x:self._addParam('out',x),t[4])
      self.typecheck(t[5])
      self._pop()

    # Assignment: check component, argument
    elif t[0] == 'ASSIGNMENT':
      self._add(t[1],self._type(t[2][0]))
      if self.error == 0:
        self._checkCompStmt(t[2])

    elif t[0] == 'THIS':
      return self._type(t)

    elif t[0] == 'OTHER':
      return self._type(t)

    elif t[0] == 'COMP':
      self._checkCompStmt(t[1])
      return self._type(['OTHER',t[1][0],t[2],t[3]])

    elif t[0] == 'INT':
      return 'Int'

    elif t[0] == 'FLOAT':
      return 'Float'

    elif t[0] == 'STRING':
      return 'String'

    # Connection: check variables
    elif t[0] == 'CONNECTION':
      if self._type(t[1]) != self._type(t[2]):
        if self.error == 0:
          print "%s TYPE SELF.ERROR[connection]: %s:%s, %s:%s" \
              % (t[2][-1][2], self.showArg(t[1]), self._type(t[1])   \
                            , self.showArg(t[2]), self._type(t[2]))
          self.error = 1

    # Controller: check variable, component
    elif t[0] == 'CONTROLLER':
      add(t[2],self._type(t[1]))
    
    # Something is missing
    else:
      pass

  def _showArg(a):
    if a[0] == 'THIS':
      return a[1] + "." + a[2][1]
    elif a[0] == 'OTHER':
      return a[1][1] + "." + a[2] + "." + a[3][1]
    elif a[0] == 'COMP':
      return a[1][0][1] + "." + a[2] + "." + a[3][1]
    else:
      return a[1]
