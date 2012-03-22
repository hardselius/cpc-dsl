import copy

from plyparser import Coord
import ast

#---------------------------------------------------------------------
# Error Handling
#---------------------------------------------------------------------

class TypeError(Exception): pass

class ReferenceError(Exception): pass

def _error_type(coord,msg):
  raise TypeError("%s: %s" % (coord,msg))

def _error_ref(coord,msg):
  raise ReferenceError("%s: %s" % (coord,msg))

#---------------------------------------------------------------------
# Typechecker
#---------------------------------------------------------------------

class TypeChecker:
  def __init__(self):
    self.env = [{}]

  #-------------------------------------------------------------------
  # Environment
  #-------------------------------------------------------------------
  
  def getEnv(self):
    return self.env[-1]


  # Close scope
  def _pop(self):
    self.env.pop()


  # Open new scope
  def _put(self):
    return self.env.append(copy.copy(self.getEnv()))


  # Add (Iden,Type) to the self.environment
  def _add(self,ident,type):
    if self._varExist(ident.name):
      _error_ref(ident,"multiple defenitions of " + ident.pos)
    else:
      self.getEnv()[ident.name] = type


  # Return the type of an Ident
  def _type(self,o):
    try:
      if   type(o) == ast.Ident:
        return self.getEnv()[o.name]

      elif type(o) == ast.This:
        return self.getEnv()[o.io][o.ident.name]

      elif type(o) == ast.Other:
        return self._typeParams(self.getEnv()[o.component.name][o.io] \
                               ,o.ident.name)

      elif type(o) == ast.Comp:
        return self._typeParams(self.getEnv()[o.component.ident.name] \
                                             [o.io], o.ident.name)

    except KeyError:
      _error_ref(ident[2],"variable is not defined: " + \
                          self._showArg(ident))


  # Returns type of a parameter 'p' from a list of parameters
  def _typeParams(self,params,p):
    for x in params:
      if x.ident.name == p: return x.type


  # Returns if variable exists in self.environment
  def _varExist(self,var):
    return self.getEnv().has_key(var)


  # Add parameter to input/output record
  def _addParam(self,param):
    if type(param) == ast.InParameter: io = 'in'
    else: io = 'out'

    if self.getEnv()[io].has_key(param.ident.name):
      _error_ref(param.ident.pos,"multiple defenitions of " + \
                 param.ident.name)

    elif param.default != None and param.type != param.default.type.title():
      _error_type(param.ident.pos,"(%s::%s) (%s::%s)" % \
                 (param.ident.name, param.type          \
                 ,param.default.value, param.default.type))

    else:
      self.getEnv()[io][param.ident.name] = param.type


  def _showArg(self,a):
    if   type(a) == ast.This:
      return a.io + "." + a.ident.name
    elif type(a) == ast.Other:
      return a.component.name + "." + a.io + "." + a.ident.name
    elif type(a) == ast.Comp:
      return a.component.component.name + "." + a.io + "." + a.ident.name
    else:
      return a.name

  #---------------------------------------------------------------------
  # typecheck function
  #---------------------------------------------------------------------

  def typecheck(self,t):
    # Program: check import, components
    if type(t) == ast.Program:
      map(self.typecheck,t.components)
      ctx = copy.copy(self.getEnv())
      self.env = [{}]
      return ctx

    # Component: check paramaters, network/atom
    elif type(t) == ast.Component:
      self._add(t.header.ident,{'in':t.header.inputs \
                              , 'out':t.header.outputs})
      self._put()
      self._add(ast.Ident('in'),{})
      self._add(ast.Ident('out'),{})
      map(self._addParam,t.header.inputs)
      map(self._addParam,t.header.outputs)
      self.typecheck(t.body)
      self._pop()

    # Network: check controller, network block
    elif type(t) == ast.Network:
      self.typecheck(t.controller)
      map(self.typecheck,t.body)

    # Network: check controller, network block
    elif type(t) == ast.Atom:
      pass

    # Assignment: check component, argument
    elif type(t) == ast.Assignment:
      self._add(t.ident,self._type(t.component.ident))
      self.typecheck(t.component)

    elif type(t) == ast.ComponentStmt:
      args = copy.copy(self._type(t.ident)['in'])
      for x in t.inputs:
        if args == []:
          _error_ref(x.ident.pos,"input out of bounds: " + \
                           self._showArg(x))
        else:
          y = args.pop(0)
          tx = self.typecheck(x)
          if tx != y.type:
            _error_type(x.ident.pos,"(%s::%s) (%s::%s)" % \
                       (self._showArg(x), tx     \
                       ,self._showArg(ast.Other(y.ident,'in',t.ident)) \
                                     ,y.type))

    elif type(t) == ast.Const:
      return t.type

    elif type(t) == ast.This:
      return self._type(t)

    elif type(t) == ast.Other:
      return self._type(t)

    elif type(t) == ast.Comp:
      self.typecheck(t.component)
      return self._type(t)

    # Connection: check variables
    elif type(t) == ast.Connection:
      if self._type(t.left) != self._type(t.right):
        _error_type(t.right.ident.pos,"(%s::%s) (%s::%s)" %         \
                   (self._showArg(t.left), self._type(t.left) \
                   ,self._showArg(t.right), self._type(t.right)))

    # Controller: check variable, component
    elif type(t) == ast.Controller:
      add(t.ident,self._type(t.type))
    
    # Something is missing
    else:
      pass
