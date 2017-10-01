from django.shortcuts import render
from .models import condPost,rulePost
from operator import eq, ne, ge, gt, le, lt
from django.contrib import messages
# import json

def cond_index(request):
    return render(request, 'conditions/index.html')

def go_admin(request):
    return render(request)

def cond_home(request):
    return render(request, 'conditions/index.html')

def cond_enq(request):
    fields = condPost.objects.order_by().values_list('field',flat=True).distinct()
    opers = condPost.objects.order_by().values_list('oper', flat=True).distinct()
    values = condPost.objects.order_by().values_list('valuetext', flat=True).distinct()
    ruleList = []
    if request.method == "POST":
        field=request.POST.get('fieldDrp','')
        oper=request.POST.get('operDrp','')
        value = request.POST.get('valDrp','')
        fbutton = request.POST.get('filBtn','')
        ebutton = request.POST.get('editBtn', '')
        eobtn = request.POST.get('edtBtn', '')
        newrte = ''
        ruledata = ''

        condName = field + oper + value
        ruleList = {}
        rules = rulePost.objects.all()

        for rule in rules:
            if fbutton == 'Show rules with above condition' :
                condList = rule.ruletext.split(" ")
                if condName in condList:
                    ruleList[rule.ruletext] = rule.ruleInt
            elif fbutton == 'Show all rules' :
                ruleList[rule.ruletext] = rule.ruleInt

        ruleText = ruledata
        intrte = newrte

        if ebutton > ' ':
            ruleText = ebutton
            ruleData = rulePost.objects.get(ruletext = ruleText)
            intrte = ruleData.ruleInt
            return render(request, 'conditions/edit.html', {'ruleText': ruleText, 'intrte': intrte})

        if eobtn == "Update":
            comments = request.POST.get('comments', '')
            ruledata = request.POST.get('ruledata', '')
            newrte = request.POST.get('intrte', '')
            ruleObj = rulePost.objects.get(ruletext=ruledata.strip())
            ruleObj.comments = comments
            try:
                ruleObj.ruleInt = int(newrte)
                ruleObj.save()
                upmsg = "Update is successful"
            except ValueError:
                upmsg = "Please enter proper interest rate"

            ruleText = ruledata
            intrte = newrte

            return render(request, 'conditions/edit.html',{'ruleText':ruleText,'intrte':intrte,'upmsg':upmsg})

        if eobtn == "Delete":
            ruledata = request.POST.get('ruledata', '')
            ruleObj = rulePost.objects.get(ruletext=ruledata.strip())
            ruleObj.delete()

            upmsg = "This rule is deleted"

            ruleText = ruledata
            intrte = newrte

            return render(request, 'conditions/edit.html',{'ruleText':ruleText,'intrte':intrte,'upmsg':upmsg})

    return render(request, 'conditions/enquire.html',
                          {'fields': fields, 'opers': opers, 'values': values, 'ruleList': ruleList})

def cond_updt(request):
    fields = condPost.objects.order_by().values_list('field', flat=True).distinct()
    names = condPost.objects.order_by().values_list('name', flat=True).distinct()
    ruletexts = rulePost.objects.order_by().values_list('ruletext', flat=True).distinct()
    condLists = condPost.objects.all()
    listCond = []
    message = ""
    ruleText = ""
    valMsg = ""
    valsw = "Y"
    if request.method == "POST":

        field = request.POST.get('fieldDrp','')
        newField = request.POST.get('newField','')
        newOper = request.POST.get('operDrp','')
        newValue = request.POST.get('newvalue','')
        rulearea = request.POST.get('ruleArea', '')
        button = request.POST.get('shwBtn', '')
        rbutton = request.POST.get('filBtn', '')
        interest = request.POST.get('interest', '')

        for condList in condLists:
            if button == 'Show related conditions':
                if field==condList.field:
                    listCond.append(condList)
            elif button == 'Show all conditions':
                listCond.append(condList)

        if button == 'Insert above condition':
            condObj = condPost()
            condObj.name = newField.strip() + newOper.strip() + newValue.strip()
            condObj.field = newField.strip()
            condObj.oper = newOper.strip()
            condObj.valuetext = newValue.strip()

            if condObj.field > '' and condObj.valuetext > '':
                if condObj.name in names:
                    message = "Condition already exist"
                else:
                    condObj.save()
                    message = "Condition is inserted"
            else:
                message = "Please insert proper data"

        if (rbutton == 'Validate') or (rbutton == 'Insert rule'):
            ruleFields=rulearea.strip().split(" ")
            for ruleField in ruleFields:
                if (ruleField in ['(',')','and','or']) or (ruleField in names):
                    pass
                else:
                    valsw = "N"
            if valsw == "N":
                valMsg = "Please correct the rule"
            else:
                valMsg = "The rule is valid"

            if (rbutton == 'Insert rule') and (valsw == "Y"):
                rulearea = rulearea.strip()
                if rulearea in ruletexts:
                    valMsg = "Rule already exists"
                else:
                    ruleObj = rulePost()
                    ruleObj.ruletext = rulearea
                    try:
                        ruleObj.ruleInt = int(interest)
                        ruleObj.save()
                        valMsg = "The rule is inserted"
                    except ValueError:
                        valMsg = "Please enter proper interest rate"

        ruleText = rulearea
        print(ruleText)

    return render(request, 'conditions/update.html',{'fields': fields,'listCond':listCond,'message':message,'ruleText':ruleText,'valMsg':valMsg})

def check_condition(lhs, op, rhs):
    return op(lhs, rhs)

def get_lpp(request):
    fields = condPost.objects.order_by().values_list('field', flat=True).distinct()
    conds = condPost.objects.all()
    rules = rulePost.objects.all()
    intText = ""
    expr = {}

    condValues = {}
    if request.method == "POST":
        for field in fields:
            expr[field] =  request.POST.get(field,'').strip()

        for cond in conds:
            lhs = expr[cond.field]
            op = eval(cond.oper)
            rhs = cond.valuetext
            condValues[cond.name] = check_condition(lhs, op, rhs)

        minInt = 999

        for rule in rules:
            ruleExpList = rule.ruletext.strip().split(" ")
            ruleExp = ""
            for ruleExps in ruleExpList:
                if ruleExps in ["and","or","(",")"]:
                    ruleExp = ruleExp + ruleExps + " "
                else:
                    ruleExp = ruleExp + "condValues['" + ruleExps + "'] "

            if eval(ruleExp):
                if rule.ruleInt < minInt:
                    minInt = rule.ruleInt
                    ruletext = rule.ruletext
        if minInt == 999:
            intText = "This data didnt hit any LPP rule "
        else:
            intText = "Interest is " + str(minInt) + ", based on the rule " + ruletext

    return render(request, 'conditions/getlpp.html', {'fields': fields, 'intText':intText})