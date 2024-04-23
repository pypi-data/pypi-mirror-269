from sigma.conversion.state import ConversionState
from sigma.rule import SigmaRule
from sigma.conversion.base import TextQueryBackend
from sigma.processing.pipeline import ProcessingPipeline
from sigma.conditions import ConditionItem, ConditionAND, ConditionOR, ConditionNOT
from sigma.types import SigmaCompareExpression, SigmaRegularExpression, SigmaRegularExpressionFlag
from sigma.pipelines.trellixhelix import trellix_helix_pipeline
import sigma
import re
from typing import ClassVar, Dict, Tuple, Pattern, List, Any, Optional

class tqlBackend(TextQueryBackend):
    """tql backend."""
    backend_processing_pipeline: ClassVar[ProcessingPipeline] = trellix_helix_pipeline()
    name : ClassVar[str] = "tql backend"
    formats : Dict[str, str] = {
        "default": "Plaintext",
        
    }
    requires_pipeline : bool = False 

    precedence : ClassVar[Tuple[ConditionItem, ConditionItem, ConditionItem]] = (ConditionNOT, ConditionAND, ConditionOR)
    parenthesize : bool = True
    group_expression : ClassVar[str] = "({expr})"  
    # Generated query tokens
    token_separator : str = " "    
    or_token : ClassVar[str] = "OR"
    and_token : ClassVar[str] = "AND"
    not_token : ClassVar[str] = "NOT"
    eq_token : ClassVar[str] = ":" 

    # String output
    ## Fields
    ### Quoting
    field_quote : ClassVar[str] = '"' 
    field_quote_pattern : ClassVar[Pattern] = re.compile("^\\w+$") 
    field_quote_pattern_negation : ClassVar[bool] = True  

    ### Escaping
    field_escape : ClassVar[str] = "\\" 
    field_escape_quote : ClassVar[bool] = True 
    field_escape_pattern : ClassVar[Pattern] = re.compile("\\s") 
    ## Values
    str_quote       : ClassVar[str] = '"'
    escape_char     : ClassVar[str] = "\\" 
    wildcard_multi  : ClassVar[str] = "*" 
    wildcard_single : ClassVar[str] = "*" 
    add_escaped     : ClassVar[str] = "\\" 
    filter_chars    : ClassVar[str] = ""  
    bool_values     : ClassVar[Dict[bool, str]] = { 
        True: "true",
        False: "false",
    }

    # String matching operators. if none is appropriate eq_token is used.
    contains_expression   : ClassVar[str] = "{field} : {value}"

    # Regular expressions
    re_expression : ClassVar[str] = "{field}:\"{regex}\""
    re_escape_char : ClassVar[str] = "\\"
    re_escape : ClassVar[Tuple[str]] = ()
    re_escape_escape_char : bool = True
    re_flag_prefix : bool = True

    #CIDR
    cidr_expression : ClassVar[str] = "{field}:{value} "

    # Numeric comparison operators
    compare_op_expression : ClassVar[str] = "{field} {operator} {value}" 
    # Mapping between CompareOperators elements and strings used as replacement for {operator} in compare_op_expression
    compare_operators : ClassVar[Dict[SigmaCompareExpression.CompareOperators, str]] = {
        SigmaCompareExpression.CompareOperators.LT  : "<",
        SigmaCompareExpression.CompareOperators.LTE : "<=",
        SigmaCompareExpression.CompareOperators.GT  : ">",
        SigmaCompareExpression.CompareOperators.GTE : ">=",
    }

    # Null/None expressions
    #field_null_expression : ClassVar[str] = "missing({field})"          # Expression for field has null value as format string with {field} placeholder for field name

    # Field existence condition expressions.
    field_exists_expression : ClassVar[str] = "has({field})"
    field_not_exists_expression : ClassVar[str] = "missing({field})"
    field_null_expression: ClassVar[str] = "missing({field})"

    # Field value in list, e.g. "field in (value list)" or "field containsall (value list)"
    convert_or_as_in : ClassVar[bool] = True                    
    convert_and_as_in : ClassVar[bool] = False #TODO                   
    in_expressions_allow_wildcards : ClassVar[bool] = True    
    field_in_list_expression : ClassVar[str] = "{field} {op} [{list}]"  
    or_in_operator : ClassVar[str] = ":"               # Operator used to convert OR into in-expressions. Must be set if convert_or_as_in is set
    #and_in_operator : ClassVar[str] = "contains-all"    # TODO
    list_separator : ClassVar[str] = ","               # List element separator

    # Value not bound to a field
    unbound_value_str_expression : ClassVar[str] = '"{value}"'
    unbound_value_num_expression : ClassVar[str] = '{value}' 

