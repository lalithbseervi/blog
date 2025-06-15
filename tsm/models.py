from django.db import models

# Create your models here.
class Node(models.Model):
    id = models.CharField(primary_key=True, max_length=256)
    rel = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    node_type = models.CharField(max_length=256)

    def __str__(self):
        return self.id
    
    @property
    def tooltip_info(self):
        rel_map = {
            'self': 'is you',
            'brother': 'is your brother',
            'father': 'is your father',
            'mother': 'is your mother',
            'grandmother': 'is your grandmother',
            'grandfather': 'is your grandfather',
            'badapappa': 'is your badapappa',
            'acquaintance': 'is your acquaintance',
            'acquaintance_m': 'is your mutual acquaintance',
            'neighbour': 'is your neighbour',
            'school': 'is where you completed SSLC',
            'puc': 'is where you completed PUC',
            'home': 'is your permanent residence'
        }
        return rel_map.get(self.rel, 'has unknown relation')
    
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source.id} -> {self.target.id}"