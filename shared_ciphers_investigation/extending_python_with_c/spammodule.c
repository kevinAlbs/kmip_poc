#define PY_SSIZE_T_CLEAN
// #define Py_REF_DEBUG
#include <Python.h>


static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    if (sts != 0) {
        // Assume error.
        PyErr_SetString(PyExc_RuntimeError, "system call returned non-zero value");
        return NULL;
    }
    return PyLong_FromLong(sts);
}

static PyObject *
spam_callme(PyObject *self, PyObject *args)
{
    PyObject *cb;
    if (!PyArg_ParseTuple(args, "O:set_callback", &cb)) {
        return NULL;
    }
    if (!PyCallable_Check (cb)) {
        PyErr_SetString(PyExc_TypeError, "argument must be callable");
        return NULL;
    }

    PyObject *result = PyObject_CallObject(cb, NULL);

    return result;
}

static PyObject* spam_rewrite_string(PyObject *self, PyObject *args) {
    Py_buffer buf;
    if (!PyArg_ParseTuple(args, "z*", &buf)) {
        return NULL;
    }
    printf ("here is buf contents: %s\n", (const char*)buf.buf);
    // TODO: is it OK to modify input buffer?
    char *ptr = (char*) buf.buf;
    ptr[0] = 'b';
    return Py_BuildValue("i", 123);
}

static PyObject* spam_goof(PyObject *self, PyObject *args) {
    printf("spam_goof is called\n");
    PyObject *obj = Py_BuildValue("s", "foobar");
    // Py_INCREF (obj);
    Py_DECREF (obj);
    Py_DECREF (obj);
    Py_DECREF (obj);
    Py_DECREF (obj);
    
    printf ("spam_goof is returning\n");
    // Py_DECREF (obj);
    return obj;
}

static PyMethodDef SpamMethods[] = {
    {"system",  spam_system, METH_VARARGS,
     "Execute a shell command."},
    {"callme",  spam_callme, METH_VARARGS,
     "Call the passed callback."},
    {"rewrite_string",  spam_rewrite_string, METH_VARARGS,
     "Rewrite the passed string."},
    {"goof",  spam_goof, METH_VARARGS,
     "Do goofy behavior."},      
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}