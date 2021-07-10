# Generated by Django 3.2.5 on 2021-07-10 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='수정일')),
                ('deleted_yn', models.CharField(blank=True, default=0, max_length=1, null=True, verbose_name='삭제여부')),
                ('room_hash', models.CharField(max_length=80, unique=True, verbose_name='방 해시값')),
                ('activate', models.BooleanField(verbose_name='매칭 기능 활성화 여부')),
                ('room_name', models.CharField(max_length=50, verbose_name='방 이름')),
                ('max_planner', models.IntegerField(verbose_name='기획자 정원')),
                ('max_designer', models.IntegerField(verbose_name='디자이너 정원')),
                ('max_frontend', models.IntegerField(verbose_name='프론트엔드 정원')),
                ('max_backend', models.IntegerField(verbose_name='백엔드 정원')),
                ('max_aosdev', models.IntegerField(verbose_name='AOS 개발자 정원')),
                ('max_iosdev', models.IntegerField(verbose_name='iOS 개발자 정원')),
            ],
            options={
                'verbose_name': '채팅방',
                'db_table': 'room',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='수정일')),
                ('deleted_yn', models.CharField(blank=True, default=0, max_length=1, null=True, verbose_name='삭제여부')),
                ('content', models.TextField(blank=True, verbose_name='채팅 내용')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.room', verbose_name='채팅방')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='사용자')),
            ],
            options={
                'verbose_name': '메시지',
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='수정일')),
                ('deleted_yn', models.CharField(blank=True, default=0, max_length=1, null=True, verbose_name='삭제여부')),
                ('position', models.CharField(blank=True, max_length=10, verbose_name='포지션')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.room', verbose_name='채팅방')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='사용자')),
            ],
            options={
                'verbose_name': '매칭풀',
                'db_table': 'match',
            },
        ),
    ]
