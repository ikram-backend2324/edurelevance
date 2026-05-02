from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subject, Topic


@login_required
def subject_list(request):
    from django.db.models import Q
    subjects = Subject.objects.prefetch_related('topics').filter(
        Q(is_public=True) | Q(created_by=request.user)
    ).distinct().order_by('name')
    return render(request, 'subjects/list.html', {'subjects': subjects})

@login_required
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if not subject.is_public and subject.created_by != request.user:
        from django.http import Http404
        raise Http404

    # Use filter with Q objects instead of union to avoid PK issues
    from django.db.models import Q
    topics = Topic.objects.filter(
        subject=subject
    ).filter(
        Q(is_public=True) | Q(created_by=request.user)
    ).distinct()

    return render(request, 'subjects/detail.html', {
        'subject': subject,
        'topics': topics
    })


@login_required
def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if not topic.is_public and topic.created_by != request.user:
        from django.http import Http404
        raise Http404
    resources = topic.resources.select_related('score').order_by('-score__score')
    return render(request, 'subjects/topic_detail.html', {
        'topic': topic,
        'resources': resources
    })


@login_required
def create_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        if name:
            subject = Subject.objects.create(
                name=name,
                description=description,
                created_by=request.user,
                is_public=False  # user's own, not public
            )
            from django.contrib import messages
            messages.success(request, f"'{name}' fani yaratildi!")
            return __import__('django.shortcuts', fromlist=['redirect']).redirect('subjects:detail', pk=subject.pk)
    from django.contrib import messages
    messages.error(request, "Fan nomi bo'sh bo'lishi mumkin emas.")
    return __import__('django.shortcuts', fromlist=['redirect']).redirect('subjects:list')


@login_required
def create_topic(request, subject_pk):
    from django.shortcuts import redirect
    from django.contrib import messages
    subject = get_object_or_404(Subject, pk=subject_pk)
    if not subject.is_public and subject.created_by != request.user:
        from django.http import Http404
        raise Http404
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        if name:
            topic = Topic.objects.create(
                subject=subject,
                name=name,
                description=description or name,
                created_by=request.user,
                is_public=False
            )
            messages.success(request, f"'{name}' mavzusi yaratildi!")
            return redirect('subjects:topic_detail', pk=topic.pk)
    messages.error(request, "Mavzu nomi bo'sh bo'lishi mumkin emas.")
    return redirect('subjects:detail', pk=subject_pk)