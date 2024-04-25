import ast
from sys import argv
from os.path import abspath, dirname, join
import argparse
from pathlib import Path


here = abspath(dirname(__file__))


template = """
var assert = require("chai").assert;
var CPU = require("../src/cpu");


Status = {
    C: 0b00000001, // Carry
    Z: 0b00000010, // Zero
    I: 0b00000100, // Interrupt Disable
    D: 0b00001000, // Decimal
    B: 0b00010000, // B Flag
    U: 0b00100000, // Unused always pushed as 1
    V: 0b01000000, // Overflow
    N: 0b10000000, // Negative
}

REGISTER_MAP = {
    'PC': 'REG_PC',
    'SP': 'REG_SP',
    'A': 'REG_ACC',
    'X': 'REG_X',
    'Y': 'REG_Y',
}

FLAG_MAP = {
    'C': 'F_CARRY',
    'Z': 'F_ZERO',
    'I': 'F_INTERRUPT',
    'D': 'F_DECIMAL',
    'V': 'F_OVERFLOW',
    'N': 'F_SIGN',
}

var MMAP = function (mem) {
    this.mem = mem;
};

MMAP.prototype.load = function (addr) {
    return this.mem[addr];
};

MMAP.prototype.write = function (addr, val) {
    this.mem[addr] = val;
};

var NES = function (mmap) {
    this.mmap = mmap;
};

NES.prototype.stop = function () {
};

describe("CPU", function () {
    var cpu = null;
    var mmap = null;
    var nes = null;
    var mem = null;
    var perform_check_cycles = true;

    before(function (done) {
        mem = Array.apply(
            null, Array(0x10000)
        ).map(Number.prototype.valueOf, 0);

        mmap = new MMAP(mem);
        nes = new NES(mmap);
        cpu = new CPU(nes);
        cpu.reset();
        cpu.mem = mem;
        perform_check_cycles = true;
        done();
    });

    function check_cycles() {
        return perform_check_cycles;
    }

    function skip_cycles() {
        perform_check_cycles = false;
    }

    function cpu_pc(counter) {
        cpu.REG_PC = counter - 1;
        cpu.REG_PC_NEW = counter - 1;
    };

    function memory_set(pos, val) {
        if (pos < 0x2000) {
            mem[pos & 0x7ff] = val;
        } else {
            nes.mmap.write(pos);
        }
    }

    function memory_fetch(pos) {
        if (pos < 0x2000) {
            return cpu.mem[pos]
        } else {
            return nes.mmap.read();
        }
    }

    function execute() {
        var cycles = cpu.emulate();
        return cycles
    }

    function cpu_set_register(register, value) {
        if (register == 'P') {
            cpu.setStatus(value);
        } else {
            var reg = REGISTER_MAP[register];
            cpu[reg] = value;
        }
    }

    function cpu_register(register) {
        if (register == 'P') {
            return cpu.getStatus();
        }
        var reg = REGISTER_MAP[register];
        var val = cpu[reg];
        if (register == 'PC') {
            return val + 1;
        }
        return val
    }

    function cpu_flag(flag){
        var fg = FLAG_MAP[flag]
        val = Boolean(cpu[fg])
        if (flag == 'Z') {
            return !val;
        }
        return val
    }

    function cpu_set_flag(flag){
        var fg = FLAG_MAP[flag];
        cpu[fg] = 1;
    }      

    function cpu_unset_flag(flag){
        var fg = FLAG_MAP[flag];
        cpu[fg] = 0;
    }

    function cpu_push_byte(byte){
        cpu.push(byte);
    }

    function cpu_pull_byte(){
        return cpu.pull();
    }

    function cpu_push_word(word){
        hi = 0xFF00 & word;
        lo = 0x00FF & word;
        cpu_push_byte(hi);
        cpu_push_byte(lo);
    }

    function cpu_pull_word() {
        var b1 = self.cpu_pull_byte()
        var b2 = self.cpu_pull_byte() << 8
        return b1 + b2
    }

%s
    
});
"""


class JSNesChaiTransformer(ast.NodeTransformer):
    def __init__(self):
        self.output = []
        self.ident_spaces = 4
        self.identation = 0
        self.skip_tests = {}

    @property
    def ident(self):
        return ' ' * self.ident_spaces * self.identation

    def append(self, code):
        self.output.append(self.ident + code)

    def translate(self, python_code, skip_tests=None):
        if skip_tests:
            self.skip_tests = skip_tests
        tree = ast.parse(python_code)
        self.visit(tree)
        return '\n'.join(self.output)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor_method = getattr(self, method_name, self.generic_visit)
        return visitor_method(node)

    def generic_visit(self, node):
        raise NotImplementedError(
            f'Visit method not implemented for {type(node).__name__}'
        )

    def visit_Module(self, node: ast.Module):
        for stmt in node.body:
            self.visit(stmt)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        pass

    def visit_Expr(self, node: ast.Expr):
        return self.visit(node.value)

    def visit_Name(self, node: ast.Name):
        return node.id

    def visit_Constant(self, node: ast.Constant):
        return node.value

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == 'CPU6502Spec':
            self.identation += 1
            for stmt in node.body:
                self.visit(stmt)
            self.identation -= 1

    def visit_FunctionDef(self, node: ast.FunctionDef):
        skip = False
        if (
            len(node.decorator_list) == 1
            and node.decorator_list[0].func.id == 'skip'
        ):
            skip_call = self.visit(node.decorator_list[0])
            skip = True
        elif node.name in self.skip_tests:
            skip_call = self.skip_tests[node.name]
            skip = True
        if node.name.startswith('test_'):
            itname = ' '.join(node.name[5:].split('_'))
            self.append(f'it("{itname}", function(done) {{')
            self.identation += 1
            if skip:
                self.append(f'{skip_call};')
            for stmt in node.body:
                call = self.visit(stmt)
                self.append(f'{call};')
            self.append('done();')
            self.identation -= 1
            self.append('});')
            self.append('')

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Attribute):
            func = node.func.attr
            if func == 'assertEqual':
                func = 'assert.equal'
            elif func == 'assertTrue':
                func = 'assert.isTrue'
            elif func == 'assertFalse':
                func = 'assert.isFalse'
        elif isinstance(node.func, ast.Name):
            func = node.func.id
        fargs = []
        for arg in node.args:
            actual = self.visit(arg)
            if isinstance(arg, ast.Call):
                fargs.append(actual)
            elif isinstance(arg, ast.Name):
                fargs.append(actual)
            elif isinstance(arg, ast.BinOp):
                fargs.append(actual)
            elif isinstance(actual, int):
                fargs.append(f'0x{actual:x}')
            elif isinstance(actual, str):
                fargs.append(f'"{actual}"')

        call_args = ', '.join(fargs)

        return f'{func}({call_args})'

    def visit_BinOp(self, node: ast.BinOp):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if isinstance(node.op, ast.BitOr):
            op = '|'
        elif isinstance(node.op, ast.Sub):
            op = '-'
        else:
            raise Exception('unknow op', op)

        return f'0x{left:x} {op} {right}'

    def visit_Attribute(self, node: ast.Attribute):
        klass = node.value.id
        attr = node.attr
        return f'{klass}.{attr}'

    def visit_Tuple(self, node: ast.Tuple):
        return 'cycles'
        # return super().visit_Tuple(node)

    def visit_Assign(self, node: ast.Assign):
        if isinstance(node.value, ast.Call):
            right = self.visit(node.value)
        if len(node.targets) == 1:
            left = self.visit(node.targets[0])
        return f'{left} = {right}'

    def visit_If(self, node: ast.If):
        test = self.visit(node.test)
        self.append(f'if ({test}) {{')
        self.identation += 1
        for stmt in node.body:
            s = self.visit(stmt)
            self.append(f'{s};')
        self.identation -= 1
        return '}'


class SkipVisitor(ast.NodeVisitor):
    def __init__(self):
        self.test_skip = {}

    def find(self, python_code):
        tree = ast.parse(python_code)
        self.visit(tree)
        return self.test_skip

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if len(node.decorator_list) == 1:
            decorator = node.decorator_list[0]
            if (
                isinstance(decorator, ast.Name)
                and decorator.id == 'skip_cycles'
            ):
                func = 'skip_cycles()'
            else:
                call = node.decorator_list[0]
                if len(call.args) == 1:
                    func = f'this.skip("{call.args[0].value}")'
                else:
                    func = 'this.skip()'
            self.test_skip[node.name] = func


def generate_chai_test(output='cpu.spec.js'):
    test_impl_file = join(here, 'tests', 'jsnes_cpu_test.py')
    with open(test_impl_file) as fp:
        test_source = fp.read()
    skipper = SkipVisitor()
    test_skip = skipper.find(test_source)
    jnes_chai = JSNesChaiTransformer()
    source_file = join(here, 'cpu_6502_spec.py')
    with open(source_file) as fp:
        source = fp.read()
    snippet = jnes_chai.translate(source, test_skip)
    code = template % snippet
    with open(output, 'w') as fp:
        fp.write(code)


# Define the list of possible types
VALID_TYPES = ['jsnes']


def main(argv):
    parser = argparse.ArgumentParser(description='Generate output files.')

    # Adding the required positional argument
    parser.add_argument(
        'test', metavar='FILE', type=str, help='The input test file'
    )

    # Adding the optional output argument
    parser.add_argument(
        '-o',
        '--output',
        metavar='OUTPUT_FILE',
        type=str,
        help='Output file name',
    )

    # Adding the required argument for type
    parser.add_argument(
        '-t',
        '--type',
        metavar='TYPE',
        type=str,
        choices=VALID_TYPES,
        required=True,
        help='Type of the file. Choose from: ' + ', '.join(VALID_TYPES),
        default='jsnes',
    )

    try:
        args = parser.parse_args(argv[1:])
        test = args.test
        output = args.output
        type = args.type

        generate_chai_test(output)

    except argparse.ArgumentError as e:
        parser.print_help()
        exit(1)


if __name__ == '__main__':
    main(argv)
