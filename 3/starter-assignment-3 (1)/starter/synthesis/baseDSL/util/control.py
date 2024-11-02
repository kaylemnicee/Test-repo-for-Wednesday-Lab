from __future__  import annotations


from typing import TYPE_CHECKING

from synthesis.baseDSL.mainBase.node import Node





if TYPE_CHECKING:
	from synthesis.baseDSL.util.factory import Factory





class Control():
    
	def __init__(self) -> None:
		pass
		
	@staticmethod
	def save(n : Node) -> str:
		ls = []
		n.save(ls)
		s =""
		s+=ls[0]
		for i in range(1,len(ls)):
			s+=";"+ls[i]
		return s
	
	@staticmethod
	def load(s:str, f: Factory) -> Node:
		ls= s.split(";")
		ls.pop(0)
		program =  f.build_S()
		program.load(ls,f)
		return program

	
	@staticmethod
	def aux_load(s:str, f:Factory) -> Node:
		if   "S"   == s : return f.build_S()
		if   "S_S"   == s : return f.build_S_S()
		if   "For_S"   == s : return f.build_For_S()
		if   "If_B_then_S_else_S"   == s : return f.build_If_B_then_S_else_S()
		if   "If_B_then_S"   == s : return f.build_If_B_then_S()
		if   "Empty"   == s : return f.build_Empty()
		if   "C"   == s : return f.build_C()
		if   "B"   == s : return f.build_B()
		if   "Attack"   == s : return f.build_Attack()
		if   "Build"   == s : return f.build_Build()
		if   "Harvest"   == s : return f.build_Harvest()
		if   "AttackIfrange"   == s : return f.build_AttackIfrange()
		if   "MoveAway"   == s : return f.build_MoveAway()
		if   "MoveToUnit"   == s : return f.build_MoveToUnit()
		if   "Train"   == s : return f.build_Train()

		#if   "CanAttack"   == s : return f.build_CanAttack()
		#if   "CanHarvest"   == s : return f.build_CanHarvest()
		#if   "HasLessNumberOfUnits"   == s : return f.build_HasLessNumberOfUnits()
		#if   "HasNumberOfUnits"   == s : return f.build_HasNumberOfUnits()
		#if   "HasNumberOfWorkersHarvesting"   == s : return f.build_HasNumberOfWorkersHarvesting()
		#if   "HasUnitInOpponentRange"   == s : return f.build_HasUnitInOpponentRange()
		#if   "HasUnitThatKillsInOneAttack"   == s : return f.build_HasUnitThatKillsInOneAttack()
		#if   "HasUnitWithinDistanceFromOpponent"   == s : return f.build_HasUnitWithinDistanceFromOpponent()
		#if   "HaveQtdUnitsAttacking"   == s : return f.build_HaveQtdUnitsAttacking()
		#if   "IsBuilder"   == s : return f.build_Is_Builder()
		#if   "is_Type"   == s : return f.build_is_Type()
		#if   "OpponentHasNumberOfUnits"   == s : return f.build_OpponentHasNumberOfUnits()
		#if   "OpponentHasUnitInPlayerRange"   == s : return f.build_OpponentHasUnitInPlayerRange()
		#if   "OpponentHasUnitThatKillsUnitInOneAttack"   == s : return f.build_OpponentHasUnitThatKillsUnitInOneAttack()