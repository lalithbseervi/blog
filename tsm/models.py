from django.db import models

# Create your models here.
class Node(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    rel = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
    
class NodeAttribute(models.Model):
    node = models.ForeignKey(Node, related_name='attributes', on_delete=models.CASCADE)
    key = models.CharField(max_length=128)
    value_text = models.TextField(blank=True, null=True)
    value_int = models.IntegerField(blank=True, null=True)
    value_date = models.DateField(blank=True, null=True)
    value_bool = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.node.id} - {self.key}"
    
    def value(self):
        return self.value_text or self.value_bool or self.value_int or self.value_date
    
class Link(models.Model):
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='source_rels')
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='target_rels')

    def __str__(self):
        return f"{self.source.id} -> {self.target.id}"