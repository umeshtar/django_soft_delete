from django.db.models import ManyToOneRel, OneToOneRel, CASCADE, PROTECT, ManyToManyField, ManyToManyRel


class DjangoSoftDelete:

    def __init__(self, model_class, pks):
        self.model_name = self.get_model_name(model_class)
        self.objs = model_class.objects.filter(pk__in=pks)

        self.protect, self.cascade = dict(), []
        self.protect_recur, self.cascade_recur = [], []
        self.summary = dict()

    @staticmethod
    def get_model_name(obj):
        return obj._meta.verbose_name

    @staticmethod
    def get_inst_name(inst):
        return str(inst)

    @staticmethod
    def get_fields(obj):
        return obj._meta.get_fields()

    def check_delete(self):
        self.protect_recur = []
        self.__get_protected(self.objs)
        self.__get_protected_msg()
        if not self.protect:
            self.cascade_recur = []
            self.cascade = self.__get_cascaded(self.model_name, self.objs)
            self.__get_cascaded_msg('', self.cascade, 0)

    def delete(self):
        self.protect_recur = []
        self.__get_protected(self.objs)
        if not self.protect:
            self.cascade_recur = []
            self.__delete(self.objs)

    def __delete(self, objs):
        for obj in objs:
            if obj not in self.cascade_recur:
                self.cascade_recur.append(obj)
                obj.is_del = True
                obj.save()
                for row in self.get_fields(obj):
                    if isinstance(row, ManyToOneRel) or isinstance(row, OneToOneRel):
                        if row.on_delete == CASCADE:
                            related_objs = row.related_model.objects.filter(is_del=False, **{f'{row.field.name}': obj})
                            self.__delete(related_objs)

    def __get_protected(self, objs):
        for obj in objs:
            if obj not in self.protect_recur:
                self.protect_recur.append(obj)
                for row in self.get_fields(obj):
                    if isinstance(row, ManyToOneRel) or isinstance(row, OneToOneRel):
                        if row.on_delete == PROTECT:
                            related_model_name = self.get_model_name(row.related_model)
                            for inst in row.related_model.objects.filter(is_del=False, **{f'{row.field.name}': obj}):
                                if related_model_name not in self.protect:
                                    self.protect[related_model_name] = [self.get_inst_name(inst)]
                                elif inst not in self.protect[related_model_name]:
                                    self.protect[related_model_name].append(self.get_inst_name(inst))
                        elif row.on_delete == CASCADE:
                            self.__get_protected(row.related_model.objects.filter(is_del=False, **{f'{row.field.name}': obj}))

    def __get_protected_msg(self):
        for model_name, objs in self.protect.items():
            print(f"{model_name}: {', '.join(objs)}")

    def __get_cascaded(self, model_name, objs):
        lst = []
        for obj in objs:
            if obj not in self.cascade_recur:
                self.cascade_recur.append(obj)
                name = self.get_model_name(type(obj))
                if name not in self.summary:
                    self.summary[name] = 1
                else:
                    self.summary[name] += 1
                lst2 = []
                for row in self.get_fields(obj):
                    if isinstance(row, ManyToOneRel) or isinstance(row, OneToOneRel):
                        if row.on_delete == CASCADE:
                            related_model_name = self.get_model_name(row.related_model)
                            related_objs = row.related_model.objects.filter(**{f'{row.field.name}': obj})
                            lst2.extend(self.__get_cascaded(related_model_name, related_objs))
                    elif isinstance(row, ManyToManyField):
                        related_model_name = self.get_model_name(row.related_model)
                        related_objs = getattr(obj, row.name).all()
                        for inst in related_objs:
                            lst2.append({
                                'model': related_model_name,
                                'name': self.get_inst_name(inst),
                                'relationship': True
                            })
                    elif isinstance(row, ManyToManyRel):
                        related_model_name = self.get_model_name(row.related_model)
                        related_objs = row.related_model.objects.filter(**{f'{row.field.name}': obj})
                        for inst in related_objs:
                            lst2.append({
                                'model': related_model_name,
                                'name': self.get_inst_name(inst),
                                'relationship': True
                            })
                lst.append({
                    'model': model_name,
                    'name': self.get_inst_name(obj),
                    'children': lst2
                })
        return lst

    def __get_cascaded_msg(self, parent_model_name, cascaded, level):
        for dic in cascaded:
            model_name = dic['model']
            inst_name = dic['name']
            is_related = dic.get('relationship', False)
            children = dic.get('children', None)
            if is_related is True:
                print(" " * level + f"{parent_model_name}-{model_name} Relationship: {inst_name}")
            else:
                print(" " * level + f"{model_name}: {inst_name}")
            if children:
                self.__get_cascaded_msg(model_name, children, level + 2)


