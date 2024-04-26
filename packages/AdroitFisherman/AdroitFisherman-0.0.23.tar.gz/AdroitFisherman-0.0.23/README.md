# 总览
## 安装
```
pip install AdroitFisherman
```
## API内部对象
### 1、常量定义
```c++
typedef PyObject* ElemType;
```
### 2、SeqListObject结构
```c++
typedef struct
{
    PyObject_HEAD
        ElemType* elem;
    int length;
    int size;
}SeqList;
```
### 3、SeqListObject插槽相关函数定义
#### (1)tp_new
```c++
static PyObject* SeqList_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    SeqList* list;
    list = (SeqList*)type->tp_alloc(type, 0);
    if (list == NULL)
    {
        PyErr_SetString(PyExc_Exception, "list object created failure!");
        return NULL;
    }
    else
    {
        list->elem = NULL;
        list->length = 0;
        list->size = 0;
        return (PyObject*)list;
    }
}
```
#### (2)tp_dealloc
```c++
static void SeqList_destroy(SeqList* self)
{
    Py_DECREF(self->elem);
    printf("DEBUG:[any_thread]-- This object has been released!");
    Py_TYPE(self)->tp_free(self);
}
```
#### (3)tp_new
```c++
static PyObject* SeqList_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    SeqList* list;
    list = (SeqList*)type->tp_alloc(type, 0);
    if (list == NULL)
    {
        PyErr_SetString(PyExc_Exception, "list object created failure!");
        return NULL;
    }
    else
    {
        list->elem = NULL;
        list->length = 0;
        list->size = 0;
        return (PyObject*)list;
    }
}
```
#### (4)tp_init
```c++
static int SeqList_init(SeqList* self, PyObject* args, PyObject* kwds)
{
    Py_INCREF(self);
    return 0;
}
```
### 4、SeqListObject内部成员定义
```c++
static PyMemberDef SeqList_members[] = {
    {"elem",T_OBJECT,offsetof(SeqList,elem),0,""},
    {"length",T_INT,offsetof(SeqList,length),0,""},
    {"size",T_INT,offsetof(SeqList,size),0,""},
    {NULL}
};
```
### 5、SeqListObject内部方法定义
```c++
static PyMethodDef SeqList_methods[] = {
    {"init_list",InitList,METH_VARARGS,""},
    {"destroy_list",DestroyList,METH_VARARGS,""},
    {"clear_list",ClearList,METH_VARARGS,""},
    {"list_empty",ListEmpty,METH_VARARGS,""},
    {"list_length",ListLength,METH_VARARGS,""},
    {"get_elem",GetElem,METH_VARARGS,""},
    {"list_insert",ListInsert,METH_VARARGS,""},
    {"list_delete",ListDelete,METH_VARARGS,""},
    {"traverse_list",TraverseList,METH_VARARGS,""},
    {NULL}
};
```