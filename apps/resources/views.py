import threading
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Resource, RelevanceScore
from .forms import ResourceForm
from apps.nlp.extractor import extract_text
from apps.nlp.scorer import evaluate_relevance


def _score_resource(resource):
    """Run scoring in background thread."""
    try:
        result = evaluate_relevance(
            topic_name=resource.topic.name,
            topic_description=resource.topic.description,
            resource_title=resource.title,
            resource_text=resource.raw_text
        )
        RelevanceScore.objects.create(
            resource=resource,
            topic=resource.topic,
            score=result['score'],
            label=result['label'],
            reason=result['reason'],
            key_matches=result.get('key_matches', []),
            missing_topics=result.get('missing', [])
        )
        resource.is_evaluated = True
        resource.save()
    except Exception:
        pass


@login_required
def upload_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user

            # Sarlavha avtomatik to'ldirish
            if not resource.title:
                if resource.resource_type == 'pdf' and resource.file:
                    resource.title = resource.file.name.split('/')[-1].replace('.pdf', '').replace('_', ' ').replace('-', ' ')
                elif resource.resource_type == 'url' and resource.url:
                    resource.title = resource.url[:80]
                else:
                    resource.title = f"{resource.topic.name} — resurs"

            # Extract text based on type
            try:
                if resource.resource_type == 'pdf':
                    raw_text = extract_text(file=resource.file)
                elif resource.resource_type == 'url':
                    raw_text = extract_text(url=resource.url)
                else:
                    raw_text = resource.text_content or ''
                resource.raw_text = raw_text
            except Exception:
                resource.raw_text = resource.text_content or ''

            resource.save()

            # Score in background — don't block the response
            thread = threading.Thread(target=_score_resource, args=(resource,))
            thread.daemon = True
            thread.start()

            messages.success(request, "Resurs yuklandi! Baholash amalga oshirilmoqda, biroz kuting...")
            return redirect('subjects:topic_detail', pk=resource.topic.pk)
        else:
            messages.error(request, "Formda xato mavjud.")
    else:
        topic_id = request.GET.get('topic')
        initial = {}
        if topic_id:
            initial['topic'] = topic_id
        form = ResourceForm(initial=initial)

    return render(request, 'resources/upload.html', {'form': form})


@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, 'resources/detail.html', {'resource': resource})


@login_required
def delete_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk, uploaded_by=request.user)
    topic_pk = resource.topic.pk
    resource.delete()
    messages.success(request, "Resurs o'chirildi.")
    return redirect('subjects:topic_detail', pk=topic_pk)


@login_required
def reevaluate_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        try:
            result = evaluate_relevance(
                topic_name=resource.topic.name,
                topic_description=resource.topic.description,
                resource_title=resource.title,
                resource_text=resource.raw_text
            )
            RelevanceScore.objects.update_or_create(
                resource=resource,
                defaults={
                    'topic': resource.topic,
                    'score': result['score'],
                    'label': result['label'],
                    'reason': result['reason'],
                    'key_matches': result.get('key_matches', []),
                    'missing_topics': result.get('missing', [])
                }
            )
            resource.is_evaluated = True
            resource.save()
            return JsonResponse({'success': True, 'score': int(result['score'] * 100), 'label': result['label']})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': "Faqat POST so'rov"})