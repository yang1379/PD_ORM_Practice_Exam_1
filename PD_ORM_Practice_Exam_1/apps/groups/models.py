# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from django.db import models
from datetime import datetime

AGE_REGEX = re.compile(r'^(\d+)$')

class UserManager(models.Manager):
    def validate(self, post_data):
        errors = {}

        if len(post_data['name']) < 2:
            errors['name'] = "The name field must only consists of letters and must be at least 2 letters long."
            
        if not re.match(AGE_REGEX, post_data['age']):
            errors['age'] = "The age field must only consists of numbers and cannot be blank."
        
        if len(errors) == 0:
            name_input = post_data['name']
            age_input = post_data['age']
            
            users = User.objects.filter(name=name_input, age=age_input)
            
            if len(users) > 0:
                user = users[0]
            else:
                user = User.objects.create(name=name_input, age=age_input)
                user.save()
            return user
        
        return errors

    def get_age_group_count(self):
        groups = {}
        
        group_count = User.objects.filter(age__range=(0, 10)).count()
        groups['0-10'] = group_count
        
        group_count = User.objects.filter(age__range=(11, 18)).count()
        groups['11-18'] = group_count
        
        group_count = User.objects.filter(age__range=(19, 24)).count()
        groups['19-24'] = group_count
        
        group_count = User.objects.filter(age__range=(25, 35)).count()
        groups['25-35'] = group_count
        
        group_count = User.objects.filter(age__range=(36, 50)).count()
        groups['36-50'] = group_count
        
        group_count = User.objects.filter(age__gte=51).count()
        groups['51+'] = group_count
        
        top_three = []
        
        count = 1
        for key in sorted(groups, key=groups.get, reverse=True):
#         for key in sorted(groups, key=groups.get):
#             top_three[key] = groups[key]
            top_three.append({key: groups[key]})
            count += 1
            if count > 3:
                break;
#             print key, groups[key]
        
        return top_three

    
    def get_group_members(self, min, max):
        if int(max) != 0:
            result = User.objects.filter(age__range=(int(min), int(max)))
        else:
            result = User.objects.filter(age__gte=51)
        
        print result
        return result
        
class CommentManager(models.Manager):
    def validate(self, post_data, name_input, age_input):
        errors = {}

        # verify all form fields contain values
        for key, value in post_data.iteritems():
            if len(value) < 1:
                errors[key] = "{} field cannot be empty".format(key)

        if len(errors) == 0:
            users = User.objects.filter(name=name_input, age=age_input)
            user_input = users[0]
            
            comment_input = post_data['comment']
            print user_input
            print "comment_input: {}".format(comment_input)
            comment = Comment.objects.create(content=comment_input, user=user_input)
#             users = User.objects.filter(name=name_input, age=age_input)
#             user_input = users[0]
            comment.save()
            return comment

        return errors
    
    def get_group_comments(self, min, max):
        comments = Comment.objects.all()
        result = []
        for comment in comments:
            if max != 0:
                if comment.user.age >= min and comment.user.age <= max:
                    result.append(comment)
            else:
                if comment.user.age >= min:
                    result.append(comment)
        return result
    
class User(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    objects = UserManager()
    
    def __str__(self):
        return "<User object - name: {}; age: {}; comment: {};".format(self.name, self.age, self.comment)
    
    def __repr__(self):
        return "<User object - name: {}; age: {}; comment: {};".format(self.name, self.age, self.comment)
    
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='comment')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    objects = CommentManager()
    
    def __str__(self):
        return "<Comment object - content: {}".format(self.content)
    
    def __repr__(self):
        return "<Comment object - content: {}".format(self.content)