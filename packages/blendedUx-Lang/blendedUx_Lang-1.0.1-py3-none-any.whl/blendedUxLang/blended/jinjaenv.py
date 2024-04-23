import sys
import re
import datetime
import ast

from collections import Mapping
from numbers import Number
from functools import reduce

import jinja2
import jinja2.ext
import jinja2.sandbox

from jinja2 import nodes
from jinja2.runtime import Undefined, Macro
from jinja2.environment import TemplateExpression
from jinja2._compat import encode_filename, string_types, iteritems,\
     text_type, imap
from jinja2.utils import Markup
from jinja2.defaults import BLOCK_START_STRING,\
    BLOCK_END_STRING, VARIABLE_START_STRING, VARIABLE_END_STRING,\
    COMMENT_START_STRING, COMMENT_END_STRING, LINE_STATEMENT_PREFIX,\
    LINE_COMMENT_PREFIX, TRIM_BLOCKS, NEWLINE_SEQUENCE,\
    KEEP_TRAILING_NEWLINE, LSTRIP_BLOCKS

from blendedUxLang.blended.functions import builtins
from blendedUxLang.blended.trimfloat import trimfloat, trimint

datetime_isoformat = "%Y-%m-%dT%H:%M:%SZ"
numbers_default_string_format = "%g"

class BlendedTemplate(jinja2.environment.Template):
    """Template class for Blended"""
    spontaneous_environments = jinja2.utils.LRUCache(10)

    def __new__(cls, source,
                block_start_string=BLOCK_START_STRING,
                block_end_string=BLOCK_END_STRING,
                variable_start_string=VARIABLE_START_STRING,
                variable_end_string=VARIABLE_END_STRING,
                comment_start_string=COMMENT_START_STRING,
                comment_end_string=COMMENT_END_STRING,
                line_statement_prefix=LINE_STATEMENT_PREFIX,
                line_comment_prefix=LINE_COMMENT_PREFIX,
                trim_blocks=TRIM_BLOCKS,
                lstrip_blocks=LSTRIP_BLOCKS,
                newline_sequence=NEWLINE_SEQUENCE,
                keep_trailing_newline=KEEP_TRAILING_NEWLINE,
                extensions=(),
                optimized=True,
                undefined=Undefined,
                finalize=None,
                autoescape=False,
                trim_floats=True,
                dict_attrs=False):
        # only changed this to use BlendedEnvironment
        env = cls.get_spontaneous_blended_environment(
            block_start_string, block_end_string, variable_start_string,
            variable_end_string, comment_start_string, comment_end_string,
            line_statement_prefix, line_comment_prefix, trim_blocks,
            lstrip_blocks, newline_sequence, keep_trailing_newline,
            frozenset(extensions), optimized, undefined, finalize, autoescape,
            trim_floats, dict_attrs, None, 0, False, None)
        return env.from_string(source, template_class=cls)

    @classmethod
    def get_spontaneous_blended_environment(cls, *args):
        """This is just implemented here to be able to use BlendedEnvironment"""
        try:
            env = cls.spontaneous_environments.get(args)
        except TypeError:
            return BlendedEnvironment(*args)
        if env is not None:
            return env
        cls.spontaneous_environments[args] = env = BlendedEnvironment(*args)
        env.shared = True
        return env

    def new_context(self, vars=None, shared=False, locals=None, args=None):
        """Reimplementation of Template.new_context,
        needed for handling Include node args.
        """
        if args:
            new_locals = dict(locals) if locals else {}
            for key, value in iteritems(args):
                new_locals['l_' + key] = value
        else:
            new_locals = locals

        return jinja2.runtime.new_context(self.environment, self.name, self.blocks,
                                          vars, shared, self.globals, new_locals)

###
### Extensions and Filters
###

class ParentExtension(jinja2.ext.Extension):
    """Extension for Parent tag."""
    tags = set(['parent'])

    def parse(self, parser):
        """
        """
        lineno = next(parser.stream).lineno
        name_node = nodes.Name('super', 'load', lineno=lineno)
        call_node = nodes.Call(name_node, [], [], None, None, lineno=lineno)
        outp_node = nodes.Output([call_node], lineno=lineno)
        return outp_node

class IfblockExtension(jinja2.ext.Extension):
    """Extension for ifblock tag."""
    tags = set(['ifblock'])

    def parse(self, parser):
        """
        Parser method for ifblock tag
        """
        lineno = parser.stream.expect('name:ifblock').lineno

        params = self.get_inline_params(parser.stream)
        node = result = nodes.If(lineno=lineno)
        param_count = len(params)

        if param_count == 1:
            node.test = self.build_test(params[0], lineno)
        else:
            node.test = self.get_or_expr(params, param_count-1, lineno)

        node.body = parser.parse_statements(('name:else', 'name:endifblock'))
        token = next(parser.stream)
        if token.test('name:else'):
            node.else_ = parser.parse_statements(('name:endifblock',), drop_needle=True)
        else:
            node.else_ = []
        return result

    def get_or_expr(self, params, index, lineno):
        if index == 0:
            return self.build_test(params[0], lineno)
        return nodes.Or(self.get_or_expr(params, index-1, lineno), self.build_test(params[index], lineno), lineno=lineno)

    def build_test(self, block_name, lineno):
        """
        """
        name_node = nodes.Name('self', 'load', lineno=lineno)
        attr_node = nodes.Getattr(name_node, block_name, 'load', lineno=lineno)
        call_node = nodes.Call(attr_node, [], [], None, None, lineno=lineno)
        return nodes.Filter(call_node, 'trim', [], [], None, None, lineno=lineno)

    def get_inline_params(self, parser_stream):
        params = []
        while(parser_stream.current.type != 'block_end' ):
            if (parser_stream.current.type == 'name'):
                params.append(parser_stream.current.value)
                next(parser_stream)
            else:
                raise jinja2.exceptions.TemplateSyntaxError("Expected block name.")
        return params

class CommentExtension(jinja2.ext.Extension):
    """Extension for comment tag."""
    tags = set(['comment'])

    def parse(self, parser):
        token = parser.stream.current
        lineno = next(parser.stream).lineno
        if token.type == 'name' and token.value == 'comment':
            parser.parse_statements(['name:endcomment'], drop_needle=True)
            return nodes.Const("")
        else:
            jinja2.exceptions.TemplateSyntaxError("Expected token 'comment'")

def items_filter(dict_val):
    """iterate over the given object and list of tuple in key, value
    representation.
    """
    if not dict_val:
        return []
    try:
        keys = sorted(dict_val.keys())
    except:
        keys = dict_val.keys()
        keys.sort()
    return [(key, dict_val[key]) for key in keys]

def number_filter(value, default=0):
    """Convert the value into an number. basically in float type
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

@jinja2.evalcontextfilter
def render_filter(eval_ctx, template, context=None):
    """renders the context in the template object.
    """
    if context is None:
        context = {}
    elif not isinstance(context, dict):
        raise TypeError("The `render` filter can only be passed a dict as an argument.")
    if hasattr(template, 'render'):
        return template.render(context)
    else:
        raise TypeError("The `render` filter should only be "
                        "applied to objecst that implement `render`.")

def datetime_filter(obj, formatting=None):
    """this filter accepts string, list or dates and return a datetime object.
    """
    if isinstance(obj, datetime.datetime):
        return obj
    elif isinstance(obj, text_type):
        if formatting:
            return datetime.datetime.strptime(obj, formatting)
        else:
            return datetime.datetime.strptime(obj, datetime_isoformat)
    elif isinstance(obj, list):
        return datetime.datetime(*imap(int, obj), tzinfo=None)

class TemplateNull(object):
    """object of class represents 'null' which is replacing None in string_filter
    """
    def __repr__(self):
        return "null"

class TemplateTrue(object):
    """object of class represents 'true' which is replacing True in string_filter
    """
    def __repr__(self):
        return "true"

class TemplateFalse(object):
    """object of class represents 'false' which is replacing False in string_filter
    """
    def __repr__(self):
        return "false"

null = TemplateNull()
true = TemplateTrue()
false = TemplateFalse()


def string_filter(value, format=None, recursion=False):

    try:  # try except block to fix the absence of unicode in py3
        if value and isinstance(value, unicode):
            value = value.encode('utf-8')
    except NameError:
        pass

    if format:
        if isinstance(value, Number) and not isinstance(value, bool):
            return format % value
        if isinstance(value, str):
            return format % trimfloat(value)
        elif isinstance(value, datetime.datetime):
            return datetime.datetime.strftime(value, format)
        elif isinstance(value, (list, tuple)):
            rendered = []
            for item in value:
                rendered.append(string_filter(item))
            return format % tuple(rendered)
        else:
            format % string_filter(value)
    else:
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, str):
            if recursion:
                return "'%s'" % value
            else:
                return "%s" % value
        elif isinstance(value, Number):
            return str(trimfloat(value))
        elif isinstance(value, datetime.datetime):
            return datetime.datetime.strftime(value, datetime_isoformat)
        elif isinstance(value, (list, tuple)):
            rendered = []
            for item in value:
                rendered.append(string_filter(item, recursion=True))
            return "[%s]" % ", ".join(rendered)
        elif isinstance(value, dict):
            rendered = []
            for key in sorted(value.keys()):
                rendered_value = string_filter(value[key], recursion=True)
                rendered.append('\'%s\': %s' % (key, rendered_value))
            return "{%s}" % ", ".join(rendered)
        else:
            raise TypeError("Type %s unsupported by string filter" % value.__class__)

filters = {
    "render": render_filter,
    "items": items_filter,
    "number": number_filter,
    "string": string_filter,
    "datetime": datetime_filter,
}
from jinja2.exceptions import UndefinedError
class BlendedEnvironment(jinja2.sandbox.SandboxedEnvironment):
    """Environment class for blended.
    """
    template_class = BlendedTemplate
    EXTENSIONS = [CommentExtension, ParentExtension, IfblockExtension,
                  jinja2.ext.do, jinja2.ext.with_, jinja2.ext.autoescape]

    def __init__(self,
                 block_start_string=BLOCK_START_STRING,
                 block_end_string=BLOCK_END_STRING,
                 variable_start_string=VARIABLE_START_STRING,
                 variable_end_string=VARIABLE_END_STRING,
                 comment_start_string=COMMENT_START_STRING,
                 comment_end_string=COMMENT_END_STRING,
                 line_statement_prefix=LINE_STATEMENT_PREFIX,
                 line_comment_prefix=LINE_COMMENT_PREFIX,
                 trim_blocks=TRIM_BLOCKS,
                 lstrip_blocks=LSTRIP_BLOCKS,
                 newline_sequence=NEWLINE_SEQUENCE,
                 keep_trailing_newline=True,
                 extensions=(),
                 optimized=True,
                 undefined=Undefined,
                 finalize=None,
                 autoescape=True,
                 loader=None,
                 cache_size=400,
                 auto_reload=True,
                 bytecode_cache=None,
                 trim_floats=True,
                 sandboxed_access=True,
                 dict_attrs=False):
        """
        The new extensions and functions are added to the environment here
        """

        self.trim_floats = trim_floats
        self.dict_attrs = dict_attrs
        self.sandboxed_access = sandboxed_access
        extensions = list(extensions)
        extensions.extend(self.EXTENSIONS)
        super(BlendedEnvironment, self).__init__(block_start_string,
                                                 block_end_string,
                                                 variable_start_string,
                                                 variable_end_string,
                                                 comment_start_string,
                                                 comment_end_string,
                                                 line_statement_prefix,
                                                 line_comment_prefix,
                                                 trim_blocks,
                                                 lstrip_blocks,
                                                 newline_sequence,
                                                 keep_trailing_newline,
                                                 extensions,
                                                 optimized,
                                                 undefined,
                                                 finalize,
                                                 autoescape,
                                                 loader,
                                                 cache_size,
                                                 auto_reload,
                                                 bytecode_cache)

        self.globals.update(builtins())
        self.globals.update({"null": None})

        def template_filter(template):
            """filter to create template from the string"""
            if isinstance(template, jinja2.environment.Template):
                return template
            elif isinstance(template, string_types):
                return self.from_string(template)
            else:
                raise TypeError("The `template` filter must only operate on "
                                "strings or template instances.")

        self.filters['template'] = template_filter
        self.filters.update(filters)

    def __substitute(self, val):
        """Substitution of verbaim to raw performs here
        """
        if re.match(r'''{%\s*verbatim\s*%}(.*?){%\s*endverbatim\s*%}''',
                    val.group(0), re.S):
            return "{%% raw %%}%s{%% endraw %%}" % val.group(1)
        elif re.match(r'''{%\s*verbatim\s*%}''', val.group(0)):
            return "{% raw %}"

    def __add_newline(self, val):
        """New line after endverbatim tag checks here
        If it newline followed by endverbatim tag this regex
        add an additional newline after endverbatim so single
        newline remove when trim_block is true
        """
        content = val.group(1)
        if re.match('\n.*', content, re.S):
            return "{%% endverbatim %%}\n%s" % content
        else:
            return "{%% endverbatim %%}%s" % content

    def preprocess(self, source, name=None, filename=None):
        """Preprocesses the source with all extensions.  This is automatically
        called for all parsing and compiling methods but *not* for :meth:`lex`
        because there you usually only want the actual source tokenized.
        Regex for conversion of verbatim to raw tag.
        """

        if self.trim_blocks:
            source = re.sub(r'''{%\s*endverbatim\s*%}(\n.*?)''', self.__add_newline, source, re.S)
        ptrn = r'''(?s)(?:{%\s*verbatim\s*%}(.*?))?{%\s*endverbatim\s*%}|{%\s*verbatim\s*%}'''
        source = re.sub(ptrn, self.__substitute, source, re.S)

        return reduce(lambda s, e: e.preprocess(s, name, filename),
                      self.iter_extensions(), text_type(source))

    def _parse(self, source, name, filename):
        """overridden to change Parser to BlendedParser"""
        return BlendedParser(self, source, name, encode_filename(filename)).parse()

    def _generate(self, source, name, filename, defer_init=False):
        """
        Should be same algorithm as superclass, but with BlendedCodeGenerator instead.
        This is the place to look at the compiled code.
        """
        if not isinstance(source, nodes.Template):
            raise TypeError('Can\'t compile non template nodes')

        generator = BlendedCodeGenerator(self, name, filename, defer_init=defer_init)
        generator.visit(source)
        result = generator.stream.getvalue()

        return result

    def compile_expression(self, source, undefined_to_none=True):
        """Should be same algorithm as superclass, but with BlendedParser instead"""
        ## Is this ever called ?
        parser = BlendedParser(self, source, state='variable')
        exc_info = None
        try:
            expr = parser.parse_expression()
            if not parser.stream.eos:
                raise jinja2.exceptions.TemplateSyntaxError('chunk after expression',
                                                            parser.stream.current.lineno,
                                                            None, None)
            expr.set_environment(self)
        except jinja2.exceptions.TemplateSyntaxError:
            exc_info = sys.exc_info()
        if exc_info is not None:
            self.handle_exception(exc_info, source_hint=source)
        body = [nodes.Assign(nodes.Name('result', 'store'), expr, lineno=1)]
        template = self.from_string(nodes.Template(body, lineno=1))
        return TemplateExpression(template, undefined_to_none)

    def _trimfloat(self, value):
        """
        trimfloat method to remove fractional part from float value.
        """
        if value==None:
            return trimint(0)
        if self.trim_floats and isinstance(value, Number) and not (isinstance(value, bool) or isinstance(value, complex)):
            if isinstance(value, int):
                return trimint(value)
            else:
                return trimfloat(value)
        try:
            if float(value):
                return trimfloat(value)
        except Exception:
            pass
          
        return value
        

    def getattr(self, obj, attribute):
        """
        """
        if not self.dict_attrs and isinstance(obj, Mapping):
            try:
                return self._trimfloat(obj[attribute])
            except (TypeError, LookupError):
                return self.undefined(obj=obj, name=attribute)
        if self.sandboxed_access:
            return self._trimfloat(super(BlendedEnvironment, self).getattr(obj, attribute))
        else:
            CurrentEnv = self.__class__
            while object not in CurrentEnv.__bases__:
                CurrentEnv = CurrentEnv.__bases__[0]
            return self._trimfloat(CurrentEnv.getattr(self, obj, attribute))

    def getitem(self, obj, argument):
        """
        """
        if not self.dict_attrs and isinstance(obj, Mapping):
            try:
                return self._trimfloat(obj[argument])
            except (TypeError, LookupError):
                return self.undefined(obj=obj, name=argument)
        return self._trimfloat(super(BlendedEnvironment, self).getitem(obj, argument))

    def call(__self, __context, __obj, *args, **kwargs):
        """
        """
        result = super(BlendedEnvironment, __self).call(__context, __obj, *args, **kwargs)
        if isinstance(__obj, Macro) and not isinstance(result, Markup):
            result = Markup(result)
        return __self._trimfloat(result)
        

    def call_filter(self, name, value, args=None, kwargs=None, context=None, eval_ctx=None):
        """
        """
        ## Does this ever get called?
        value = super(BlendedEnvironment, self).call_filter(name, value, args, kwargs,
                                                            context, eval_ctx)
        return self._trimfloat(value)


class BlendedImmutableEnvironment(BlendedEnvironment):
    '''

    '''
    def __init__(self,
                 block_start_string=BLOCK_START_STRING,
                 block_end_string=BLOCK_END_STRING,
                 variable_start_string=VARIABLE_START_STRING,
                 variable_end_string=VARIABLE_END_STRING,
                 comment_start_string=COMMENT_START_STRING,
                 comment_end_string=COMMENT_END_STRING,
                 line_statement_prefix=LINE_STATEMENT_PREFIX,
                 line_comment_prefix=LINE_COMMENT_PREFIX,
                 trim_blocks=TRIM_BLOCKS,
                 lstrip_blocks=LSTRIP_BLOCKS,
                 newline_sequence=NEWLINE_SEQUENCE,
                 keep_trailing_newline=True,
                 extensions=(),
                 optimized=True,
                 undefined=Undefined,
                 finalize=None,
                 autoescape=False,
                 loader=None,
                 cache_size=400,
                 auto_reload=True,
                 bytecode_cache=None,
                 trim_floats=True,
                 sandboxed_access=True,
                 dict_attrs=True):
                 
        super(BlendedImmutableEnvironment, self).__init__(block_start_string,
                 block_end_string, variable_start_string, variable_end_string,
                 comment_start_string, comment_end_string, line_statement_prefix,
                 line_comment_prefix, trim_blocks, lstrip_blocks, newline_sequence,
                 keep_trailing_newline, extensions, optimized, undefined,
                 finalize, autoescape, loader, cache_size, auto_reload,
                 bytecode_cache,trim_floats,sandboxed_access,dict_attrs)
    
    def is_safe_attribute(self, obj, attr, value):
        if not super(BlendedEnvironment, self).is_safe_attribute(obj, attr, value):
            return False
        return not jinja2.sandbox.modifies_known_mutable(obj, attr)


class BlendedParser(jinja2.parser.Parser):
    """
    This parser subclass overrides the parsing of the include tag, in order to provide
    a local context feature.  It also overrides parse_primary to ensure that numbers are
    printed without trailing zeros.
    """

    def _wrap_as_const(self, as_const):
        """
        """
        def as_const_wrapper(eval_ctx=None):
            """
            """
            value = as_const(eval_ctx)
            if isinstance(value, Number):
                return self.environment._trimfloat(value)
            return value
        return as_const_wrapper

    def _wrap_parse(parse_method):
        """
        """
        def parse_wrapper(self, *args, **kwargs):
            """
            """
            node = parse_method(self, *args, **kwargs)
            node.as_const = self._wrap_as_const(node.as_const)
            return node
        return parse_wrapper

    parse_primary = _wrap_parse(jinja2.parser.Parser.parse_primary)
    parse_filter = _wrap_parse(jinja2.parser.Parser.parse_filter)

    def parse_include(self):
        """
        Reimplementation of Parser.parse_include, necessary for new Include functionality
        """
        lineno = lineno = next(self.stream).lineno
        node = nodes.Include(lineno=lineno)
        node.fields = nodes.Include.fields + ('with_expression',) ## compiler needs this

        node.template = self.parse_expression()
        if self.stream.current.test('name:ignore') and\
           self.stream.look().test('name:missing'):
            node.ignore_missing = True
            self.stream.skip(2)
        else:
            node.ignore_missing = False

        node.with_expression = None
        if self.stream.current.test_any('name:with', 'name:without') and\
           self.stream.look().test('name:context'):
            node.with_context = next(self.stream).value == 'with'
            self.stream.skip()
        elif self.stream.current.test('name:with'):
            self.stream.skip()
            node.with_expression = self.parse_expression()
            if self.stream.current.test('name:only'):
                node.with_context = True
                self.stream.skip()
            else:
                node.with_context = True

        elif self.stream.current.test('name:only'):
            node.with_context = False
            self.stream.skip()
        else:
            node.with_context = True
        return node


class BlendedCodeGenerator(jinja2.compiler.CodeGenerator):
    """
    This subclass does a couple of things: it helps standardize all numbers in Jinja
    as floats, but with the feature that trailing zeroes are not printed; it also adds
    functionality to the include tag.

    What is added to include is the ability to pass specific arguments into the tag.

    .. sourcecode:: jinja

        {% include "included_file.html" with { "arg1": strval, "arg2": numval } %}
    """

    def pull_locals(self, frame):
        """
        """
        for name in frame.identifiers.undeclared:
            self.writeline('l_%s = environment._trimfloat(context.resolve(%r))' % (name, name))

    def visit_Const(self, node, frame):
        """
        """
        val = node.value
        if isinstance(val, Number):
            self.write('environment._trimfloat(' + str(val) + ')')
        else:
            self.write(repr(val))

    def visit_Filter(self, node, frame):
        """
        """
        self.write('environment._trimfloat(')
        super(BlendedCodeGenerator, self).visit_Filter(node, frame)
        self.write(')')

    def visit_Include(self, node, frame):
        """
        Handles includes. Overrides base functionality to add new Include node functionality
        """
        if node.with_context:
            self.unoptimize_scope(frame)
        if node.ignore_missing:
            self.writeline('try:')
            self.indent()

        func_name = 'get_or_select_template'
        if isinstance(node.template, nodes.Const):
            if isinstance(node.template.value, string_types):
                func_name = 'get_template'
            elif isinstance(node.template.value, (tuple, list)):
                func_name = 'select_template'
        elif isinstance(node.template, (nodes.Tuple, nodes.List)):
            func_name = 'select_template'

        self.writeline('template = environment.%s(' % func_name, node)
        self.visit(node.template, frame)
        self.write(', %r)' % self.name)
        if node.ignore_missing:
            self.outdent()
            self.writeline('except TemplateNotFound:')
            self.indent()
            self.writeline('pass')
            self.outdent()
            self.writeline('else:')
            self.indent()

        if node.with_expression:
            self.writeline('args = dict(')
            self.visit(node.with_expression, frame)
            self.write(')')

            if node.with_context:
                self.writeline('vars = dict(context.parent)')
                self.writeline('ctxt = template.new_context(vars, True, locals(), args)')
            else:
                self.writeline('ctxt = template.new_context(args, True)')
            self.writeline('for event in template.root_render_func(ctxt):')
        else:
            if node.with_context:
                self.writeline('ctxt = template.new_context(context.parent, True, locals())')
                self.writeline('for event in template.root_render_func(ctxt):')
            else:
                self.writeline('for event in template.module._body_stream:')

        self.indent()
        self.simple_write('event', frame)
        self.outdent()

        if node.ignore_missing:
            self.outdent()
