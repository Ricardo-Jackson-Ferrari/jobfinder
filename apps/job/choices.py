MODALITIES = (
    ('P', 'presencial'),
    ('R', 'remoto'),
    ('H', 'híbrido'),
)

HIERARCHIES = (
    ('JA', 'Jovem Aprendiz'),
    ('EST', 'Estágio'),
    ('A', 'Auxiliar'),
    ('JR', 'Júnior'),
    ('P', 'Pleno'),
    ('S', 'Sênior'),
    ('ESP', 'Especialista'),
)

EXPERIENCIES = (
    (0, 'Nenhuma'),
    (1, '0 - 1 ano'),
    (2, '1 - 2 anos'),
    (3, '2 - 5 anos'),
    (4, '5 - 10 anos'),
    (5, 'Mais de 10 anos'),
)

PERIOD_CHOICES = (
    ('today', 'Hoje'),
    ('last_3_days', 'Últimos 3 dias'),
    ('last_week', 'Última semana'),
    ('last_2_weeks', 'Últimas 2 semanas'),
    ('last_month', 'Último mês'),
)
