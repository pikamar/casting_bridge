# -*- coding: utf-8 -*-
import os
# import click
from functools import wraps
import datetime
import sys
from PIL import Image
from werkzeug import secure_filename
from flask import request, Blueprint, render_template, json, jsonify, flash, \
    redirect, url_for, send_from_directory, config, session, Response
from casting_bridge import db, app, ALLOWED_EXTENSIONS, manager, admin
#from casting_bridge import manager
from casting_bridge.catalog.models import Classifier, Person, Skill, Document, UserForm, UpdateForm, LoginForm
from sqlalchemy.orm.util import join
from sqlalchemy import func, desc, or_
from flask.ext.admin.contrib.sqla import ModelView
from datetime import date
import pytz
import helpers
import pdfkit


reload(sys)
sys.setdefaultencoding("utf-8")

catalog = Blueprint('catalog', __name__)

# @app.cli.command()
# def alterdb():
#     """Initialize the database."""
#     click.echo('altering the db')
# add status
@catalog.route('/alter-tables-status')
def alter_tables_status():
    # flash('person [%s] ' % (db.engine.execute("SELECT status_date FROM person LIMIT 0,1;")), 'info')
    # db.engine.execute("ALTER TABLE `person` ADD `status` INT NOT NULL DEFAULT '0';")
    # images
    # db.engine.execute("ALTER TABLE `person` ADD `status` INT NULL;")
    # db.engine.execute("ALTER TABLE `person` ADD `status_date` DATE NULL;")
    db.engine.execute("ALTER TABLE `person` ADD `status_sent` INT NULL;")
    db.engine.execute("ALTER TABLE `person` ADD `status_sent_date` DATE NULL;")
    db.engine.execute("ALTER TABLE `person` ADD `status_due_date` DATE NULL;")
    db.engine.execute("ALTER TABLE `person` ADD `status_payed` INT NULL;")
    db.engine.execute("ALTER TABLE `person` ADD `status_payed_date` DATE NULL;")
    return render_template('404.html'), 200

@catalog.route('/profile-print/<id>')
def profile_print(id):
    if 'username' not in session:
        return redirect(url_for('catalog.login'))

    person = Person.query.get_or_404(id)
    form = UpdateForm(
        request.form,
        name=person.name,
        surname=person.surname,
        nickname=person.nickname,
        pcode=person.pcode,
        contract_nr=person.contract_nr,
        birthdate=person.birthdate,
        my_phone=person.my_phone,
        email=person.email,
        other_phone=person.other_phone,
        home_address=person.home_address,
        height=person.height,
        foot_size=person.foot_size,
        cloth_size=person.cloth_size,
        voice=person.voice,
        contact_lenses=person.contact_lenses,
        be_dressed=person.be_dressed,
        mother_phone_code=person.mother_phone_code,
        mother_phone=person.mother_phone,
        mother_name=person.mother_name,
        father_phone_code=person.father_phone_code,
        father_phone=person.father_phone,
        father_name=person.father_name,
        experience=person.experience,
        current_occupation=person.current_occupation,
        workplace=person.workplace,
        play_age_from=person.play_age_from,
        play_age_to=person.play_age_to
    )
    if person.species:
        form.species.data = person.species

    if person.speciality:
        form.speciality.data = person.speciality

    # Get all possible values(choices) from Classifier
    choices = list()
    city_box = Classifier.query.filter_by(category='city').all()
    for city_box in city_box:
        if city_box:
            choices.append((city_box.tag_lv, city_box.tag_lv))
    form.city.choices = choices

    choices = []
    haircolor = Classifier.query.filter_by(category='haircolor').all()
    for haircolor in haircolor:
        if haircolor:
            choices.append((haircolor.tag_lv, haircolor.tag_lv))
    form.haircolor.choices = choices

    choices = []
    eyecolor = Classifier.query.filter_by(category='eyecolor').all()
    for eyecolor in eyecolor:
        if eyecolor:
            choices.append((eyecolor.tag_lv, eyecolor.tag_lv))
    form.eyecolor.choices = choices

    choices = []
    voice = Classifier.query.filter_by(category='voice').all()
    for voice in voice:
        if voice:
            choices.append((voice.tag_lv, voice.tag_lv))
    form.voice.choices = choices

    choices = []
    co = Classifier.query.filter_by(category='current_occupation').all()
    for co in co:
        if co:
            choices.append((co.tag_lv, co.tag_lv))
    form.current_occupation.choices = choices

    choices = []
    for size in range(35, 50, 1): # filled clothe size range 35 to 49
        choices.append((str(size), (str(size))))
    form.foot_size.choices = choices

    choices = []
    for size in range(32, 69, 2): # filled clothe size range 32 to 68
        choices.append((str(size), (str(size))))
    form.cloth_size.choices = choices

    # Get all assigned Skills for person and add them as selected in form.
    classifiers = Classifier.query.select_from(join(Classifier, Skill)).filter(Skill.person_id == id)
    skill_box = {}
    for item in classifiers:
        #flash('skill [%s] cat [%s] ' % (item.tag_lv, item.category), 'info')
        if skill_box.get(item.category) is None:
            skill_box[item.category] = [(item.tag_lv, item.tag_lv)]
        else:
            skill_box[item.category].append((item.tag_lv, item.tag_lv))
    all_danceskill = ''
    all_singskill = ''
    all_musicskill = ''
    all_sportskill = ''
    all_swimskill = ''
    all_driveskill = ''
    all_languageskill = ''
    all_otherskill = ''
    all_want_participate = ''
    all_dont_want_participatee = ''
    all_interested_in = ''
    all_tattoo = ''
    all_piercing = ''
    all_afraidof = ''
    all_religion = ''
    all_educational_institution = ''
    all_learned_profession = ''
    all_degree = ''
    all_current_occupation = ''
    all_subspeciality = ''
    all_specily = ''
    all_mother = ''
    all_father = ''
    all_workplaces = ''
    #flash('danceskilldanceskill [%s]' % skill_box.get('danceskill'), 'info')
    if skill_box.get('city'):
        for skill in skill_box.get('city'):
            form.city.data = skill[0]
    if skill_box.get('haircolor'):
        for skill in skill_box.get('haircolor'):
            form.haircolor.data = skill[0]
    if skill_box.get('eyecolor'):
        for skill in skill_box.get('eyecolor'):
            form.eyecolor.data = skill[0]
    if skill_box.get('subspeciality'):
        form.subspeciality.choices = skill_box.get('subspeciality')
        for skill in skill_box.get('subspeciality'):
            all_subspeciality += str(skill[0]) + " "
    if skill_box.get('danceskill'):
        form.danceskill.choices = skill_box.get('danceskill')
        for skill in skill_box.get('danceskill'):
            all_danceskill += str(skill[0]) + " "
    if skill_box.get('singskill'):
        form.singskill.choices = skill_box.get('singskill')
        for skill in skill_box.get('singskill'):
            all_singskill += str(skill[0]) + " "
    if skill_box.get('musicskill'):
        form.musicskill.choices = skill_box.get('musicskill')
        for skill in skill_box.get('musicskill'):
            all_musicskill += str(skill[0]) + " "
    if skill_box.get('sportskill'):
        form.sportskill.choices = skill_box.get('sportskill')
        for skill in skill_box.get('sportskill'):
            all_sportskill += str(skill[0]) + " "
    if skill_box.get('swimskill'):
        form.swimskill.choices = skill_box.get('swimskill')
        for skill in skill_box.get('swimskill'):
            all_swimskill += str(skill[0]) + " "
    if skill_box.get('driveskill'):
        form.driveskill.choices = skill_box.get('driveskill')
        for skill in skill_box.get('driveskill'):
            all_driveskill += str(skill[0]) + " "
    if skill_box.get('languageskill'):
        form.languageskill.choices = skill_box.get('languageskill')
        for skill in skill_box.get('languageskill'):
            all_languageskill += str(skill[0]) + " "
    if skill_box.get('otherskill'):
        form.otherskill.choices = skill_box.get('otherskill')
        for skill in skill_box.get('otherskill'):
            all_otherskill += str(skill[0]) + " "
    if skill_box.get('want_participate'):
        form.want_participate.choices = skill_box.get('want_participate')
        for skill in skill_box.get('want_participate'):
            all_want_participate += str(skill[0]) + " "
    if skill_box.get('dont_want_participate'):
        form.dont_want_participate.choices = skill_box.get('dont_want_participate')
        for skill in skill_box.get('dont_want_participate'):
            all_dont_want_participatee += str(skill[0]) + " "
    if skill_box.get('interested_in'):
        form.interested_in.choices = skill_box.get('interested_in')
        for skill in skill_box.get('interested_in'):
            all_interested_in += str(skill[0]) + " "
    if skill_box.get('tattoo'):
        form.tattoo.choices = skill_box.get('tattoo')
        for skill in skill_box.get('tattoo'):
            all_tattoo += str(skill[0]) + " "
    if skill_box.get('piercing'):
        form.piercing.choices = skill_box.get('piercing')
        for skill in skill_box.get('piercing'):
            all_piercing += str(skill[0]) + " "
    if skill_box.get('afraidof'):
        form.afraidof.choices = skill_box.get('afraidof')
        for skill in skill_box.get('afraidof'):
            all_afraidof += str(skill[0]) + " "
    if skill_box.get('religion'):
        form.religion.choices = skill_box.get('religion')
        for skill in skill_box.get('religion'):
            all_religion += str(skill[0]) + " "
    if skill_box.get('educational_institution'):
        form.educational_institution.choices = skill_box.get('educational_institution')
        for skill in skill_box.get('educational_institution'):
            all_educational_institution += str(skill[0]) + " "
    if skill_box.get('learned_profession'):
        form.learned_profession.choices = skill_box.get('learned_profession')
        for skill in skill_box.get('learned_profession'):
            all_learned_profession += str(skill[0]) + " "
    if skill_box.get('degree'):
        form.degree.choices = skill_box.get('degree')
        for skill in skill_box.get('degree'):
            all_degree += str(skill[0]) + " "
    if skill_box.get('current_occupation'):
        form.current_occupation.choices = skill_box.get('current_occupation')
        for skill in skill_box.get('current_occupation'):
            all_current_occupation += str(skill[0]) + " "
    if skill_box.get('voice'):
        form.current_occupation.choices = skill_box.get('voice')
    if skill_box.get('cb_tags'):
        form.cb_tags.choices = skill_box.get('cb_tags')
    if skill_box.get('family_notes'):
        form.family_notes.choices = skill_box.get('family_notes')
    if skill_box.get('workplaces'):
        form.workplace.choices = skill_box.get('workplaces')
    all_mother = str(person.mother_name) \
        + ' - ' \
        + str(person.mother_phone_code) \
        + str(person.mother_phone)
    all_father = str(person.father_name) \
        + ' - ' \
        + str(person.father_phone_code) \
        + str(person.father_phone)
    if str(person.speciality) == 'actor':
        all_specily = 'Aktieris'
    if str(person.speciality) == 'professional':
        all_specily = 'Profesionālis'
    if str(person.speciality) == 'talent':
        all_specily = 'Talants'
    str_be_dressed = ''
    if person.be_dressed:
        str_be_dressed = 'Jā'
    str_contact_lenses = 'Nav'
    if person.contact_lenses:
        str_contact_lenses = 'Ir'
    str_tuks = ''
    if str(person.mother_name) == str_tuks:
        all_mother = ''
    if str(person.father_name) == str_tuks:
        all_father = ''
    cels = os.getcwd()
    html = """
    <! DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    <head>
    <title>Anketa</title>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8">
    </head>
    <body>
    <table border="0" align="center" width="100%">
    <tr><td width="20%">"""
    html += '<img src="'+ cels +'\\casting_bridge\\static\\img\\cb_logo_s.png"> '
    html += '</td><td width="80%" align=center><h1>Datu bāzes anketas</h1></td></tr><table border="0" align="center" width="100%">'
    html += '<tr><td colspan=2><h2></h2></td></tr>'
    html += ' <tr><td colspan=2  style="border-bottom:1pt solid black;">'
    html += '<table border="0" align="center" width="100%">'
    html += '<tr><td colspan=2 style="border-bottom:1pt solid black;"><font size="5"><img src="'+ cels +'\\casting_bridge\\static\\img\\cil.png">  Personas dati</font></td><td colspan=2 style="border-bottom:1pt solid black;"><font size="5"><img src="'+ cels +'\\casting_bridge\\static\\img\\groupa.png">  Ģimene</font></td></tr>'
    html += '<tr><td width="25%">Vārds:</td><td width="25%"><b> ' + str(person.name) +'</b></td><td>Mātes vārds/uzvārds:</td><td><b> ' + all_mother +'</b></td></tr>'
    html += '<tr><td width="25%">Uzvārds:</td><td width="25%"><b> ' + str(person.surname) +'</b></td><td>Tēva vārds/uzvārds:</td><td><b> ' + all_father +'</b></td></tr>'
    html += '<tr><td width="25%">Skatuves vārds:</td><td width="25%"><b> ' + str(person.nickname) +'</b></td><td>Telefons 1:</td><td><b> ' + str(person.my_phone_code)+  str(person.my_phone) +'</b></td></tr>'
    html += '<tr><td width="25%">Personas kods:</td><td width="25%"><b> ' + str(person.pcode) +'</b></td><td>Telefons 2:</td><td><b> ' + str(person.other_phone_code)+  str(person.other_phone) +'</b></td></tr>'
    html += '<tr><td width="25%">Viensošanās numurs:</td><td width="25%"><b> ' + str(person.contract_nr) +'</b></td><td>E-pasts:</td><td><b> ' + str(person.email) +'</b></td></tr>'
    html += '<tr><td width="25%">Dzimšanas datums:</td><td width="25%"><b> ' + str(person.birthdate) +'</b></td><td>Adrese:</td><td><b> ' + str(person.home_address) +'</b></td></tr>'
    html += '</table>'
    html += '</td></tr><tr><td colspan=2  style="border-bottom:1pt solid black;"> <table border="0" align="center" width="100%">'
    html += '<tr><td colspan=2 style="border-bottom:1pt solid black;"><font size="5"><img src="'+ cels +'\\casting_bridge\\static\\img\\shapes.png">  Personīgās īpašības</font></td><td colspan=2 style="border-bottom:1pt solid black;"><font size="5"><img src="'+ cels +'\\casting_bridge\\static\\img\\shape.png">  Kas tu esi?</font></td></tr>'
    html += '<tr><td width="25%">Augums:</td><td width="25%"><b> ' + str(person.height) +'</b></td><td>Kas tu esi?:</td><td><b> ' + str(all_specily) +'</b></td></tr>'
    html += '<tr><td width="25%">Apavu izmērs:</td><td width="25%"><b> ' + str(person.foot_size) +'</b></td><td>Specializācija:</td><td><b> ' + str(all_subspeciality) +'</b></td></tr>'
    html += '<tr><td width="25%">Apģērbu izmērs:</td><td width="25%"><b> ' + str(person.cloth_size) +'</b></td><td>Filmēšanas pierdze:</td><td><b> ' + str(form.experience.data) +'</b></td></tr>'
    html += '<tr><td width="25%">Balss tembrs:</td><td width="25%"><b> ' + str(person.voice) +'</b></td><td>Valodu zināšanas:</td><td><b> '+str(all_languageskill)+'</b></td></tr>'
    html += '<tr><td width="25%">Matu krāsa:</td><td width="25%"><b> ' + str(form.haircolor.data) +'</b></td><td>Hobiji:</td><td><b> '+str(all_otherskill)+'</b></td></tr>'
    html += '<tr><td width="25%">Acu krāsa:</td><td width="25%"><b> ' + str(form.eyecolor.data) +'</b></td><td> </td><td> </td></tr>'
    html += '</table></td></tr>'
    html += '<tr><td colspan=2 style="border-bottom:1pt solid black;"><table border="0" align="center" width="100%">'
    html += '<tr><td colspan=2 style="border-bottom:1pt solid black;"><font size="5"><img src="'+ cels +'\\casting_bridge\\static\\img\\music.png">  Prasmes</font></td><td colspan=2 style="border-bottom:1pt solid black;"><font size="5"><img src="'+ cels +'\\casting_bridge\\static\\img\\interface.png">  Darbs un izglītība</font></td></tr>'
    html += '<tr><td width="25%">Dejotprasme:</td><td width="25%"><b> ' + str(all_danceskill) +'</b></td><td>Mācību iestāde:</td><td><b> ' + str(all_educational_institution) +'</b></td></tr>'
    html += '<tr><td width="25%">Dziedātprasme:</td><td width="25%"><b> ' + str(all_singskill) +'</b></td><td>Apgūtā profesija:</td><td><b> ' + str(all_learned_profession) +'</b></td></tr>'
    html += '<tr><td width="25%">Mūzikas instrumenti:</td><td width="25%"><b> ' + str(all_musicskill) +'</b></td><td>Klase vai līmenis:</td><td><b> ' + str(all_degree) +'</b></td></tr>'
    html += '<tr><td width="25%">Sporta veidi:</td><td width="25%"><b> ' + str(all_sportskill) +'</b></td><td>Nodarbošanās:</td><td><b> ' + str(all_current_occupation) +'</b></td></tr>'
    html += '<tr><td width="25%">Peldētprasme:</td><td width="25%"><b> ' + str(all_swimskill) +'</b></td><td>Darba vieta:</td><td><b> ' + str(all_workplaces or person.workplace) +'</b></td></tr>'
    html += '<tr><td width="25%">Transportlīdzekļa vadīšana:</td><td width="25%"><b> ' + str(all_driveskill) +'</b></td><td> </td><td> </td></tr>'
    html += '</table></td></tr>'
    html += '<tr><td colspan=2 style="border-bottom:1pt solid black;"><table border="0" align="center" width="100%">'
    html += '<tr><td colspan=2 style="border-bottom:1pt solid black;"><font size="5"><img src="'+ cels +'\\casting_bridge\\static\\img\\check.png">  Manas vēlmes</font></td><td colspan=2 style="border-bottom:1pt solid black;"><font size="5"><img src="'+ cels +'\\casting_bridge\\static\\img\\school.png">  Piezīmes, ko jāņem vērā</font></td></tr>'
    html += '<tr><td width="25%">Gribu piedalīties:</td><td width="25%"><b> ' + str(all_want_participate) +'</b></td><td>Tetovējumi:</td><td><b> ' + str(all_tattoo) +'</b></td></tr>'
    html += '<tr><td width="25%">Negribu piedalīties:</td><td width="25%"><b> ' + str(all_dont_want_participatee) +'</b></td><td>Pīrsingi:</td><td><b> ' + str(all_piercing) +'</b></td></tr>'
    html += '<tr><td width="25%">Mani interesē:</td><td width="25%"><b> ' + str(all_interested_in) +'</b></td><td>Bailes no:</td><td><b> ' + str(all_afraidof) +'</b></td></tr>'
    html += '<tr><td width="25%">Nevēlos atkailināties kameras priekšā:</div></td><td width="25%"><b>  '+ str_be_dressed +'</b></td><td>Reliģiskā pārliecība:</td><td><b> ' + str(all_religion) +'</b></td></tr>'
    html += '<tr><td width="25%"> </td><td width="25%"> </td><td>Kontaktlēcas:</td><td><b> ' + str_contact_lenses +'</b></td></tr>'
    html += '</table> </td></tr>'
    html += '<tr><td colspan=2><div>*Ar šo izsaku savu piekrišanu, ka SIA"CASTING BRIDGE", vienotais reģistrācijas numurs: 40103389862, iekļauj, uzglabā un apstrādā savā datu bāzē manus fiziskās personas datus. Esmu informēts, ka minētās darbības nepieciešamas, lai piedāvātu manus pakalpojumus trešajām personām. Piekrītu, ka manis sniegtā informācija atlases un pakalpojumu sniegšanas gaitā tiks sniegta trešajām personām, kuras ir ieinteresētas minēto pakalpojumu pirkšanā.</div></br></td></tr>'
    html += '<tr><td width="50%"><h3>Datums:</h3></td><td width="50%"><h3>*paraksts:</h3></td></tr></table>'
    html += '</body>'
    html += '</html>'

    #path_wkthmltopdf = r'C:\Python27\wkhtmltopdf\bin\wkhtmltopdf.exe'
    #config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    fn = app.config['UPLOAD_FOLDER'] + '/documents' + str(id) + '.pdf'
    url = 'http://0.0.0.0/uploads/' + 'documents' + str(id) + '.pdf'
    #pdfkit.from_string(html,fn, configuration=config)
    pdfkit.from_string(html, fn)

    return redirect(url)


@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/uploads/profile/<path:filename>')
def profile_dir(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + "profile/", filename, as_attachment=True)

@app.route('/uploads/thumbnail/<path:filename>')
def thumbnail_dir(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + "thumbnail/", filename, as_attachment=True)

@app.route('/uploads/photo/<path:filename>')
def photo_dir(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + "photo/", filename, as_attachment=True)

@app.route('/uploads/photo/preview/<path:filename>')
def photo_direct_dir(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + "photo/", filename)

def allowed_file(filename):
    return '.' in filename and \
            filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def template_or_json(template=None):
    """"Return a dict from your view and this will either
    pass it to a template or render json. Use like:

    @template_or_json('template.html')
    """
    def decorated(f):
        @wraps(f)
        def decorated_fn(*args, **kwargs):
            ctx = f(*args, **kwargs)
            if request.is_xhr or not template:
                return jsonify(ctx)
            else:
                return render_template(template, **ctx)
        return decorated_fn
    return decorated

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@catalog.route('/data-enter', methods=['GET', 'POST'])
def create_enter():
    if 'username' not in session:
        return redirect(url_for('catalog.login'))

    form = UserForm(request.form)

    choices = list()
    want_participate_box = Classifier.query.filter_by(category='want_participate').all()
    for want_participate_box in want_participate_box:
        if want_participate_box:
            choices.append((want_participate_box.tag_lv, want_participate_box.tag_lv))
    form.want_participate.choices = choices

    choices = []
    city_box = Classifier.query.filter_by(category='city').all()
    for city_box in city_box:
        if city_box:
            choices.append((city_box.tag_lv, city_box.tag_lv))
    form.city.choices = choices

    choices = []
    haircolor = Classifier.query.filter_by(category='haircolor').all()
    for haircolor in haircolor:
        if haircolor:
            choices.append((haircolor.tag_lv, haircolor.tag_lv))
    form.haircolor.choices = choices

    choices = []
    eyecolor = Classifier.query.filter_by(category='eyecolor').all()
    for eyecolor in eyecolor:
        if eyecolor:
            choices.append((eyecolor.tag_lv, eyecolor.tag_lv))
    form.eyecolor.choices = choices

    choices = []
    voice = Classifier.query.filter_by(category='voice').all()
    for voice in voice:
        if voice:
            choices.append((voice.tag_lv, voice.tag_lv))
    form.voice.choices = choices

    choices = []
    co = Classifier.query.filter_by(category='current_occupation').all()
    for co in co:
        if co:
            choices.append((co.tag_lv, co.tag_lv))
    form.current_occupation.choices = choices

    choices = []
    for size in range(35, 50, 1): # filled clothe size range 35 to 49
        choices.append((str(size), (str(size))))
    form.foot_size.choices = choices

    choices = []
    for size in range(32, 69, 2): # filled clothe size range 32 to 68
        choices.append((str(size), (str(size))))
    form.cloth_size.choices = choices

    #   ignore object values if form submitted
    if request.form.get('csrf_token', False):
        for skill in request.form.getlist('subspeciality'):
            form.subspeciality.choices.append([skill, skill])
        for skill in request.form.getlist('danceskill'):
            form.danceskill.choices.append([skill, skill])
        for skill in request.form.getlist('singskill'):
            form.singskill.choices.append([skill, skill])
        for skill in request.form.getlist('musicskill'):
            form.musicskill.choices.append([skill, skill])
        for skill in request.form.getlist('sportskill'):
            form.sportskill.choices.append([skill, skill])
        for skill in request.form.getlist('swimskill'):
            form.swimskill.choices.append([skill, skill])
        for skill in request.form.getlist('driveskill'):
            form.driveskill.choices.append([skill, skill])
        for skill in request.form.getlist('languageskill'):
            form.languageskill.choices.append([skill, skill])
        for skill in request.form.getlist('otherskill'):
            form.otherskill.choices.append([skill, skill])
        for skill in request.form.getlist('want_participate'):
            form.want_participate.choices.append([skill, skill])
        for skill in request.form.getlist('dont_want_participate'):
            form.dont_want_participate.choices.append([skill, skill])
        for skill in request.form.getlist('interested_in'):
            form.interested_in.choices.append([skill, skill])
        for skill in request.form.getlist('tattoo'):
            form.tattoo.choices.append([skill, skill])
        for skill in request.form.getlist('piercing'):
            form.piercing.choices.append([skill, skill])
        for skill in request.form.getlist('afraidof'):
            form.afraidof.choices.append([skill, skill])
        for skill in request.form.getlist('religion'):
            form.religion.choices.append([skill, skill])
        for skill in request.form.getlist('educational_institution'):
            form.educational_institution.choices.append([skill, skill])
        for skill in request.form.getlist('learned_profession'):
            form.learned_profession.choices.append([skill, skill])
        for skill in request.form.getlist('degree'):
            form.degree.choices.append([skill, skill])
        for skill in request.form.getlist('current_occupation'):
            form.current_occupation.choices.append([skill, skill])
        for skill in request.form.getlist('workplaces'):
            form.workplaces.choices.append([skill, skill])
        for skill in request.form.getlist('voice'):
            form.current_occupation.choices.append([skill, skill])
        for skill in request.form.getlist('cb_tags'):
            form.cb_tags.choices.append([skill, skill])
        for skill in request.form.getlist('family_notes'):
            form.family_notes.choices.append([skill, skill])
    else:
        # Get all assigned Skills for person and add them as selected in form.
        classifiers = Classifier.query \
            .select_from(join(Classifier, Skill)) \
            .filter(Classifier.tag_lv == 'Nav' or Classifier.tag_lv.like('% nav'))
        skill_box = {}
        for item in classifiers:
            if skill_box.get(item.category) is None:
                skill_box[item.category] = [(item.tag_lv, item.tag_lv)]
            else:
                skill_box[item.category].append((item.tag_lv, item.tag_lv))

        form.subspeciality.choices = skill_box.get('subspeciality', [])
        form.danceskill.choices = skill_box.get('danceskill', [])
        form.singskill.choices = skill_box.get('singskill', [])
        form.musicskill.choices = skill_box.get('musicskill', [])
        form.sportskill.choices = skill_box.get('sportskill', [])
        form.swimskill.choices = skill_box.get('swimskill', [])
        form.driveskill.choices = skill_box.get('driveskill', [])
        form.languageskill.choices = skill_box.get('languageskill', [])
        form.otherskill.choices = skill_box.get('otherskill', [])
        form.tattoo.choices = skill_box.get('tattoo', [])
        form.piercing.choices = skill_box.get('piercing', [])
        form.educational_institution.choices = skill_box.get('educational_institution', [])
        form.learned_profession.choices = skill_box.get('learned_profession', [])
        form.degree.choices = skill_box.get('degree', [])
        form.current_occupation.choices = skill_box.get('current_occupation', [])
        form.workplaces.choices = skill_box.get('workplaces', [])
        form.current_occupation.choices = skill_box.get('voice', [])

    if form.validate_on_submit():
        email_addresses = form.email.data
        if request.form.get('extra_emails[]', False):
            for email_address in request.form.getlist('extra_emails[]'):
                email_addresses = email_addresses + ',' + email_address
        name = form.name.data
        surname = form.surname.data
        nickname = form.nickname.data
        pcode = form.pcode.data
        contract_nr = form.contract_nr.data
        birthdate = form.birthdate.data
        my_phone_code = form.my_phone_code.data
        my_phone = form.my_phone.data
        email = email_addresses
        other_phone_code = form.other_phone_code.data
        other_phone = form.other_phone.data
        home_address = form.home_address.data
        height = form.height.data
        foot_size = form.foot_size.data
        cloth_size = form.cloth_size.data
        voice = form.voice.data
        contact_lenses = form.contact_lenses.data
        be_dressed = form.be_dressed.data
        species = form.species.data
        mother_phone_code = form.mother_phone_code.data
        mother_phone = form.mother_phone.data
        mother_name = form.mother_name.data
        father_phone_code = form.father_phone_code.data
        father_phone = form.father_phone.data
        father_name = form.father_name.data
        speciality = form.speciality.data
        experience = form.experience.data
        city = form.city.data
        haircolor = form.haircolor.data
        eyecolor = form.eyecolor.data
        current_occupation = form.current_occupation.data
        workplace = form.workplace.data
        cb_tags = form.cb_tags.data
        family_notes = form.family_notes.data
        play_age_from = form.play_age_from.data
        play_age_to = form.play_age_to.data
        # status = form.status.data
        # status_date = form.status_date.data
        # status_sent_date = form.status_sent_date.data
        # status_due_date = form.status_due_date.data
        # status_payed = form.status_payed.data
        # status_payed_date = form.status_payed_date.data
        person = Person(
            datetime.datetime.now(pytz.timezone("Europe/Riga")),
            datetime.datetime.now(pytz.timezone("Europe/Riga")),
            name,
            surname,
            nickname,
            pcode,
            contract_nr,
            birthdate,
            my_phone_code,
            my_phone,
            email,
            other_phone_code,
            other_phone,
            home_address,
            height,
            foot_size,
            cloth_size,
            voice,
            contact_lenses,
            be_dressed,
            None,
            False,
            species,
            mother_phone_code,
            mother_phone,
            mother_name,
            father_phone_code,
            father_phone,
            father_name,
            speciality,
            experience,
            None,
            current_occupation,
            workplace,
            play_age_from,
            play_age_to
        )
        db.session.add(person)
        db.session.commit()
        skills = list()

        if city:
            skills.append(['city', city])

        if haircolor:
            skills.append(['haircolor', haircolor])

        if eyecolor:
            skills.append(['eyecolor', eyecolor])

        for subspeciality in form.subspeciality.data:
            skills.append(['subspeciality', subspeciality])

        for danceskill in form.danceskill.data:
            skills.append(['danceskill', danceskill])

        for singskill in form.singskill.data:
            skills.append(['singskill', singskill])

        for musicskill in form.musicskill.data:
            skills.append(['musicskill', musicskill])

        for sportskill in form.sportskill.data:
            skills.append(['sportskill', sportskill])

        for swimskill in form.swimskill.data:
            skills.append(['swimskill', swimskill])

        for otherskill in form.otherskill.data:
            skills.append(['otherskill', otherskill])

        for driveskill in form.driveskill.data:
            skills.append(['driveskill', driveskill])

        for languageskill in form.languageskill.data:
            skills.append(['languageskill', languageskill])

        for want_participate in form.want_participate.data:
            skills.append(['want_participate', want_participate])

        for dont_want_participate in form.dont_want_participate.data:
            skills.append(['dont_want_participate', dont_want_participate])

        for interested_in in form.interested_in.data:
            skills.append(['interested_in', interested_in])

        for tattoo in form.tattoo.data:
            skills.append(['tattoo', tattoo])

        for piercing in form.piercing.data:
            skills.append(['piercing', piercing])

        for afraidof in form.afraidof.data:
            skills.append(['afraidof', afraidof])

        for religion in form.religion.data:
            skills.append(['religion', religion])

        for educational_institution in form.educational_institution.data:
            skills.append(['educational_institution', educational_institution])

        for learned_profession in form.learned_profession.data:
            skills.append(['learned_profession', learned_profession])

        for degree in form.degree.data:
            skills.append(['degree', degree])

        for cb_tags in form.cb_tags.data:
            skills.append(['cb_tags', cb_tags])

        for family_notes in form.family_notes.data:
            skills.append(['family_notes', family_notes])

        for skill in skills:
            #flash('Skills [%s] [%s]' % (skill[0], skill[1]), 'success')
            item = Classifier.query.filter_by(
                category=skill[0],
                tag_lv=skill[1].capitalize()
            ).first()
            if item is None: # add new entry in Classifier
                item = Classifier(category=skill[0], tag_lv=skill[1].capitalize())
                db.session.add(item)
                db.session.commit()

            add_skill = Skill(person=person, classifier=item)
            db.session.add(add_skill)
            db.session.commit()

        file_mask = helpers.make_file_mask(species, birthdate, speciality, height)
        if 'images[]' in request.files:
            files = request.files.getlist('images[]')
            for uploaded_file in files:
                #flash('file: [%s]' % file.filename, 'success')
                filename = ''
                if uploaded_file and allowed_file(uploaded_file.filename):
                    filename = str(person.id) \
                        + "_" \
                        + file_mask \
                        + secure_filename(uploaded_file.filename)
                    photo_resize(uploaded_file, filename, 683, 1024, False, "photo/")
                    photo_resize(uploaded_file, filename, 250, 375, False, "thumbnail/")
                    add_document = Document(
                        datetime.datetime.now(pytz.timezone("Europe/Riga")),
                        person.id,
                        'photo',
                        filename
                    )
                    db.session.add(add_document)

        helpers.file_upload('audio', 'audio', person.id)
        helpers.file_upload('video', 'video', person.id)

        if 'profile_image' in request.files:
            profile_image = request.files['profile_image']
            if profile_image and helpers.allowed_file(profile_image.filename):
                #flash('profile_image: [%s]' % profile_image, 'success')
                filename, file_extension = os.path.splitext(secure_filename(profile_image.filename))
                filename = str(person.id) + "_profile" + file_extension
                photo_resize(profile_image, filename, 250, 250, True, "profile/")
                Person.query.filter_by(id=person.id).update({
                    'profile_image': filename
                })
        if 'cv' in request.files:
            uploaded_cv = request.files['cv']
            if uploaded_cv and helpers.allowed_file(uploaded_cv.filename):
                filename, file_extension = os.path.splitext(secure_filename(uploaded_cv.filename))
                filename = str(person.id) + "_cv" + file_extension
                uploaded_cv.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                Person.query.filter_by(id=person.id).update({
                    'cv': filename
                })

        db.session.commit()

        flash(
            'The person %s has been created' % person.id, 'success'
        )

        return redirect(
            url_for('catalog.profiles')
        )

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('data-enter.html', form=form)

@catalog.route('/update-profile/<id>', methods=['GET', 'POST'])
def update_profile(id):
    if 'username' not in session:
        return redirect(url_for('catalog.login'))

    person = Person.query.get_or_404(id)
    form = UpdateForm(
        request.form,
        created=person.created,
        name=person.name,
        surname=person.surname,
        nickname=person.nickname,
        pcode=person.pcode,
        contract_nr=person.contract_nr,
        birthdate=person.birthdate,
        my_phone=person.my_phone,
        email=person.email,
        other_phone=person.other_phone,
        home_address=person.home_address,
        height=person.height,
        foot_size=person.foot_size,
        cloth_size=person.cloth_size,
        voice=person.voice,
        contact_lenses=person.contact_lenses,
        be_dressed=person.be_dressed,
        mother_phone_code=person.mother_phone_code,
        mother_phone=person.mother_phone,
        mother_name=person.mother_name,
        father_phone_code=person.father_phone_code,
        father_phone=person.father_phone,
        father_name=person.father_name,
        experience=person.experience,
        current_occupation=person.current_occupation,
        workplace=person.workplace,
        play_age_from=person.play_age_from,
        play_age_to=person.play_age_to,
        status=person.status,
        status_date=person.status_date,
        status_sent_date=person.status_sent_date,
        status_due_date=person.status_due_date,
        status_payed=person.status_payed,
        status_payed_date=person.status_payed_date,
        is_active=person.is_active
    )

    if person.species:
        form.species.data = person.species

    if person.speciality:
        form.speciality.data = person.speciality

    # Get all possible values(choices) from Classifier
    choices = list()
    city_box = Classifier.query.filter_by(category='city').all()
    for city_box in city_box:
        if city_box:
            choices.append((city_box.tag_lv, city_box.tag_lv))
    form.city.choices = choices

    choices = []
    haircolor = Classifier.query.filter_by(category='haircolor').all()
    for haircolor in haircolor:
        if haircolor:
            choices.append((haircolor.tag_lv, haircolor.tag_lv))
    form.haircolor.choices = choices

    choices = []
    eyecolor = Classifier.query.filter_by(category='eyecolor').all()
    for eyecolor in eyecolor:
        if eyecolor:
            choices.append((eyecolor.tag_lv, eyecolor.tag_lv))
    form.eyecolor.choices = choices

    choices = []
    voice = Classifier.query.filter_by(category='voice').all()
    for voice in voice:
        if voice:
            choices.append((voice.tag_lv, voice.tag_lv))
    form.voice.choices = choices

    choices = []
    co = Classifier.query.filter_by(category='current_occupation').all()
    for co in co:
        if co:
            choices.append((co.tag_lv, co.tag_lv))
    form.current_occupation.choices = choices

    choices = []
    for size in range(35, 50, 1): # filled clothe size range 35 to 49
        choices.append((str(size), (str(size))))
    form.foot_size.choices = choices

    choices = []
    for size in range(32, 69, 2): # filled clothe size range 32 to 68
        choices.append((str(size), (str(size))))
    form.cloth_size.choices = choices

    #   ignore object values if form submitted
    if request.form.get('csrf_token', False):
        for skill in request.form.getlist('subspeciality'):
            form.subspeciality.choices.append([skill, skill])
        for skill in request.form.getlist('danceskill'):
            form.danceskill.choices.append([skill, skill])
        for skill in request.form.getlist('singskill'):
            form.singskill.choices.append([skill, skill])
        for skill in request.form.getlist('musicskill'):
            form.musicskill.choices.append([skill, skill])
        for skill in request.form.getlist('sportskill'):
            form.sportskill.choices.append([skill, skill])
        for skill in request.form.getlist('swimskill'):
            form.swimskill.choices.append([skill, skill])
        for skill in request.form.getlist('driveskill'):
            form.driveskill.choices.append([skill, skill])
        for skill in request.form.getlist('languageskill'):
            form.languageskill.choices.append([skill, skill])
        for skill in request.form.getlist('otherskill'):
            form.otherskill.choices.append([skill, skill])
        for skill in request.form.getlist('want_participate'):
            form.want_participate.choices.append([skill, skill])
        for skill in request.form.getlist('dont_want_participate'):
            form.dont_want_participate.choices.append([skill, skill])
        for skill in request.form.getlist('interested_in'):
            form.interested_in.choices.append([skill, skill])
        for skill in request.form.getlist('tattoo'):
            form.tattoo.choices.append([skill, skill])
        for skill in request.form.getlist('piercing'):
            form.piercing.choices.append([skill, skill])
        for skill in request.form.getlist('afraidof'):
            form.afraidof.choices.append([skill, skill])
        for skill in request.form.getlist('religion'):
            form.religion.choices.append([skill, skill])
        for skill in request.form.getlist('educational_institution'):
            form.educational_institution.choices.append([skill, skill])
        for skill in request.form.getlist('learned_profession'):
            form.learned_profession.choices.append([skill, skill])
        for skill in request.form.getlist('degree'):
            form.degree.choices.append([skill, skill])
        for skill in request.form.getlist('current_occupation'):
            form.current_occupation.choices.append([skill, skill])
        for skill in request.form.getlist('workplaces'):
            form.workplaces.choices.append([skill, skill])
        for skill in request.form.getlist('voice'):
            form.current_occupation.choices.append([skill, skill])
        for skill in request.form.getlist('cb_tags'):
            form.cb_tags.choices.append([skill, skill])
        for skill in request.form.getlist('family_notes'):
            form.family_notes.choices.append([skill, skill])
    else:
        # Get all assigned Skills for person and add them as selected in form.
        classifiers = Classifier.query \
            .select_from(join(Classifier, Skill)) \
            .filter(Skill.person_id == id)
        skill_box = {}
        for item in classifiers:
            if skill_box.get(item.category) is None:
                skill_box[item.category] = [(item.tag_lv, item.tag_lv)]
            else:
                skill_box[item.category].append((item.tag_lv, item.tag_lv))

        for skill in skill_box.get('city', []):
            form.city.data = skill[0]
        for skill in skill_box.get('haircolor', []):
            form.haircolor.data = skill[0]
        for skill in skill_box.get('eyecolor', []):
            form.eyecolor.data = skill[0]
        form.subspeciality.choices = skill_box.get('subspeciality', [])
        form.danceskill.choices = skill_box.get('danceskill', [])
        form.singskill.choices = skill_box.get('singskill', [])
        form.musicskill.choices = skill_box.get('musicskill', [])
        form.sportskill.choices = skill_box.get('sportskill', [])
        form.swimskill.choices = skill_box.get('swimskill', [])
        form.driveskill.choices = skill_box.get('driveskill', [])
        form.languageskill.choices = skill_box.get('languageskill', [])
        form.otherskill.choices = skill_box.get('otherskill', [])
        form.want_participate.choices = skill_box.get('want_participate', [])
        form.dont_want_participate.choices = skill_box.get('dont_want_participate', [])
        form.interested_in.choices = skill_box.get('interested_in', [])
        form.tattoo.choices = skill_box.get('tattoo', [])
        form.piercing.choices = skill_box.get('piercing', [])
        form.afraidof.choices = skill_box.get('afraidof', [])
        form.religion.choices = skill_box.get('religion', [])
        form.educational_institution.choices = skill_box.get('educational_institution', [])
        form.learned_profession.choices = skill_box.get('learned_profession', [])
        form.degree.choices = skill_box.get('degree', [])
        form.current_occupation.choices = skill_box.get('current_occupation', [])
        form.workplaces.choices = skill_box.get('workplaces', [])
        form.current_occupation.choices = skill_box.get('voice', [])
        form.cb_tags.choices = skill_box.get('cb_tags', [])
        form.family_notes.choices = skill_box.get('family_notes', [])

    photos = Document.query \
        .filter_by(person_id=id, type='photo') \
        .order_by(desc(Document.id)) \
        .paginate(1, 100, error_out=False)
    videos = Document.query \
        .filter_by(person_id=id, type='video') \
        .order_by(desc(Document.id)) \
        .paginate(1, 100, error_out=False)

    if form.validate_on_submit():
        email_addresses = form.email.data
        if request.form.get('extra_emails[]', False):
            for email_address in request.form.getlist('extra_emails[]'):
                email_addresses = email_addresses + ',' + email_address
        created = form.created.data
        name = form.name.data
        surname = form.surname.data
        nickname = form.nickname.data
        pcode = form.pcode.data
        contract_nr = form.contract_nr.data
        birthdate = form.birthdate.data
        my_phone = form.my_phone.data
        email = email_addresses
        other_phone = form.other_phone.data
        home_address = form.home_address.data
        height = form.height.data
        foot_size = request.form['foot_size']
        cloth_size = request.form['cloth_size']
        voice = request.form['voice']
        contact_lenses = form.contact_lenses.data
        be_dressed = form.be_dressed.data
        # field is set from request.form['species'], because form.species.data is already set to (old)value from db
        species = request.form['species']
        mother_phone_code = form.mother_phone_code.data
        mother_phone = form.mother_phone.data
        mother_name = form.mother_name.data
        father_phone_code = form.father_phone_code.data
        father_phone = form.father_phone.data
        father_name = form.father_name.data
        speciality = request.form['speciality']
        experience = form.experience.data
        city = request.form['city']
        haircolor = request.form['haircolor']
        eyecolor = request.form['eyecolor']
        current_occupation = request.form['current_occupation']
        workplace = form.workplace.data
        play_age_from = form.play_age_from.data
        play_age_to = form.play_age_to.data
        status = form.status.data
        status_date = form.status_date.data
        status_sent_date = form.status_sent_date.data
        status_due_date = form.status_due_date.data
        status_payed = form.status_payed.data
        status_payed_date = form.status_payed_date.data
        is_active = form.is_active.data

        Person.query.filter_by(id=id).update({
            'created': created,
            'modified': datetime.datetime.now(pytz.timezone("Europe/Riga")),
            'name': name,
            'surname': surname,
            'nickname': nickname,
            'pcode': pcode,
            'contract_nr': contract_nr,
            'birthdate': birthdate,
            'my_phone': my_phone,
            'email': email,
            'other_phone': other_phone,
            'home_address': home_address,
            'height': height,
            'foot_size': foot_size,
            'cloth_size': cloth_size,
            'voice': voice,
            'contact_lenses': contact_lenses,
            'be_dressed': be_dressed,
            'species': species,
            'mother_phone_code': mother_phone_code,
            'mother_phone': mother_phone,
            'mother_name': mother_name,
            'father_phone_code': father_phone_code,
            'father_phone': father_phone,
            'father_name': father_name,
            'speciality': speciality,
            'experience': experience,
            'current_occupation': current_occupation,
            'workplace': workplace,
            'play_age_from': play_age_from,
            'play_age_to': play_age_to,
            'status': status,
            'status_date': status_date,
            'status_sent_date' : status_sent_date,
            'status_due_date' : status_due_date,
            'status_payed' : status_payed,
            'status_payed_date' : status_payed_date,
            'is_active': is_active
        })

        skills = list()
        if city:
            skills.append(['city', city])

        if haircolor:
            skills.append(['haircolor', haircolor])

        if eyecolor:
            skills.append(['eyecolor', eyecolor])

        for subspeciality in form.subspeciality.data:
            skills.append(['subspeciality', subspeciality])

        for danceskill in form.danceskill.data:
            skills.append(['danceskill', danceskill])

        for singskill in form.singskill.data:
            skills.append(['singskill', singskill])

        for musicskill in form.musicskill.data:
            skills.append(['musicskill', musicskill])

        for sportskill in form.sportskill.data:
            skills.append(['sportskill', sportskill])

        for swimskill in form.swimskill.data:
            skills.append(['swimskill', swimskill])

        for otherskill in form.otherskill.data:
            skills.append(['otherskill', otherskill])

        for driveskill in form.driveskill.data:
            skills.append(['driveskill', driveskill])

        for languageskill in form.languageskill.data:
            skills.append(['languageskill', languageskill])

        for want_participate in form.want_participate.data:
            skills.append(['want_participate', want_participate])

        for dont_want_participate in form.dont_want_participate.data:
            skills.append(['dont_want_participate', dont_want_participate])

        for interested_in in form.interested_in.data:
            skills.append(['interested_in', interested_in])

        for tattoo in form.tattoo.data:
            skills.append(['tattoo', tattoo])

        for piercing in form.piercing.data:
            skills.append(['piercing', piercing])

        for afraidof in form.afraidof.data:
            skills.append(['afraidof', afraidof])

        for religion in form.religion.data:
            skills.append(['religion', religion])

        for educational_institution in form.educational_institution.data:
            skills.append(['educational_institution', educational_institution])

        for learned_profession in form.learned_profession.data:
            skills.append(['learned_profession', learned_profession])

        for degree in form.degree.data:
            skills.append(['degree', degree])

        for workplaces in form.workplaces.data:
            skills.append(['workplaces', workplaces])

        for cb_tags in form.cb_tags.data:
            skills.append(['cb_tags', cb_tags])

        for family_notes in form.family_notes.data:
            skills.append(['family_notes', family_notes])



        # Delete outdated skills
        Skill.query.filter_by(person_id=id).delete()
        for skill in skills:
            #flash('Skills [%s] [%s]' % (skill[0], skill[1]), 'success')
            item = Classifier.query.filter_by(category=skill[0], tag_lv=skill[1].capitalize()).first()
            if item is None: # add new entry in Classifier
                item = Classifier(category=skill[0], tag_lv=skill[1].capitalize())
                db.session.add(item)

            add_skill = Skill(person=person, classifier=item)
            db.session.add(add_skill)

        db.session.commit()

        file_mask = helpers.make_file_mask(species, birthdate, speciality, height)
        if 'images[]' in request.files:
            files = request.files.getlist('images[]')
            for uploaded_file in files:
                #flash('file: [%s]' % uploaded_file.filename, 'success')
                filename = ''
                if uploaded_file and allowed_file(uploaded_file.filename):
                    filename = str(person.id) \
                        + "_" \
                        + file_mask \
                        + secure_filename(uploaded_file.filename)
                    photo_resize(uploaded_file, filename, 683, 1024, False, "photo/")
                    photo_resize(uploaded_file, filename, 250, 375, False, "thumbnail/")
                    add_document = Document(
                        datetime.datetime.now(pytz.timezone("Europe/Riga")),
                        person.id,
                        'photo',
                        filename
                    )
                    db.session.add(add_document)

        helpers.file_upload('audio', 'audio', person.id)
        helpers.file_upload('video', 'video', person.id)
        if 'profile_image' in request.files:
            profile_image = request.files['profile_image']
            # flash('request files: [%s]' % profile_image, 'success')
            filename = ''
            if profile_image and helpers.allowed_file(profile_image.filename):
                #flash('profile_image: [%s]' % profile_image, 'success')
                filename, file_extension = os.path.splitext(secure_filename(profile_image.filename))
                filename = str(person.id) + "_profile" + file_extension
                #photo_thumbnail(profile_image, filename)
                photo_resize(profile_image, filename, 250, 250, True, "profile/")
                Person.query.filter_by(id=person.id).update({
                    'profile_image': filename
                })
        if 'cv' in request.files:
            uploaded_cv = request.files['cv']
            if uploaded_cv and helpers.allowed_file(uploaded_cv.filename):
                filename, file_extension = os.path.splitext(secure_filename(uploaded_cv.filename))
                filename = str(person.id) + "_cv" + file_extension
                uploaded_cv.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                Person.query.filter_by(id=person.id).update({
                    'cv': filename
                })

        db.session.commit()

        flash('Profile updated.', 'info')
        return redirect(url_for('catalog.profiles'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('profile_update.html', form=form, person=person, photos=photos, videos=videos)

@catalog.route('/update-profile-photo', methods=['GET'])
def update_profile_photo():
    personID = request.args.get('person')
    person = Person.query.get_or_404(personID)
    photoID = request.args.get('photo')
    photo = Document.query.get_or_404(photoID)
    date = request.args.get('date')
    if date == '':
        return Response(json.dumps({'message': 'Invalid date format'}), status=400, mimetype='application/json')

    photo.created = datetime.datetime.strptime(date, '%d-%m-%Y %H:%M:%S')
    db.session.add(photo)
    db.session.commit()

    return Response(json.dumps({'message': 'success'}), status=200, mimetype='application/json')

def photo_resize(image, filename, width, heigh, crop=False, sufolder=""):
    size = (width, heigh)
    im = Image.open(image)
    # make square image
    if crop:
        crop_size = im.width
        if im.height < im.width:
            crop_size = im.height
        im = im.crop((0,0,crop_size,crop_size))
    if im.height < im.width:
        size = (heigh, width)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(os.path.join(app.config['UPLOAD_FOLDER'] + sufolder + filename), "JPEG")

@catalog.route('/')
@catalog.route('/profiles')
@catalog.route('/profiles/<int:page>')
def profiles(page=1):
    if 'username' not in session:
        return redirect(url_for('catalog.login'))

    pid = request.args.get('id')
    phone = request.args.get('phone')
    name = request.args.get('name')
    surname = request.args.get('surname')
    city = request.args.get('city')
    species = request.args.get('species')
    speciality = request.args.get('speciality')
    age_from = request.args.get('age_from')
    age_to = request.args.get('age_to')

    profiles = Person.query
    skills = request.args.get('skills')
    anySkills = request.args.get('any_skills')
    classifiers = list()
    classifierIds = []

    if skills:
        classifierIds = skills.split(',')
        classifiers = Classifier.query.filter(Classifier.id.in_(classifierIds)).all()
    if city:
        classifierIds.append(city)

    if pid:
        profiles = profiles.filter(Person.id == pid)

    if phone:
        profiles = profiles.filter(or_(Person.my_phone.like('%' + phone + '%'), Person.other_phone.like('%' + phone + '%'), Person.mother_phone.like('%' + phone + '%'), Person.father_phone.like('%' + phone + '%')))

    if name:
        profiles = profiles.filter(Person.name.like('%' + name.title() + '%'))
    if surname:
        profiles = profiles.filter(Person.surname.like('%' + surname.title() + '%'))

    # Get all possible values(choices) from Classifier
    cities = Classifier.query.filter_by(category='city').all()

    if skills or city:
        profiles = profiles.join(Person.skills)
        profiles = profiles.filter(Skill.classifier_id.in_(classifierIds))

    if species:
        profiles = profiles.filter(Person.species == species)
    if speciality:
        profiles = profiles.filter(Person.speciality == speciality)
    if age_from and age_from.isdigit() and age_to and age_to.isdigit():
        today = date.today()
        date_from = datetime.date(today.year - int(age_from), today.month, today.day)
        date_to = datetime.date(today.year - int(age_to), today.month, today.day)
        profiles = profiles.filter(Person.birthdate >= date_to)
        profiles = profiles.filter(Person.birthdate <= date_from)

    if (skills or city) and not anySkills:
        profiles = profiles.group_by(Person.id)
        profiles = profiles.having(func.count() == len(classifierIds))

    sort = request.args.get('sort', 0)
    if sort == '1':
        sort_by = Person.created
    elif sort == '2':
        sort_by = desc(Person.created)
    elif sort == '3':
        sort_by = Person.status
    elif sort == '4':
        sort_by = desc(Person.status)
    else:
        sort_by = desc(Person.id)

    profiles = profiles.order_by(sort_by)
    paginated = profiles.paginate(page, 12)

    return render_template(
        'profiles.html', profiles=paginated, skills=classifiers, cities=cities
    )

@catalog.route('/profile-favorites')
@catalog.route('/profile-favorites/<int:page>')
def profile_favorites(page=1):
    if 'username' not in session:
        return redirect(url_for('catalog.login'))
    profiles = Person.query

    favorites = request.cookies.get('favorites')
    if favorites:
        favorites = favorites.replace('%22', '"')
        favorites = favorites.replace('%2C', ',')
        favorites = json.loads(favorites)
        profiles = profiles.filter(Person.id.in_(favorites))

    profiles = profiles.order_by(Person.name)

    return render_template(
        'profile_favorites.html', profiles=profiles.paginate(page, 12)
    )

def delete_file(filename, subfolder=""):
    name = os.path.join(app.config['UPLOAD_FOLDER'] + subfolder, filename)
    if os.path.exists(name):
        os.remove(name)

@catalog.route('/profile-delete')
def profile_delete():
    if 'username' not in session:
        return redirect(url_for('catalog.login'))

    id = request.args.get('id')
    person = Person.query.get_or_404(id)

    # Delete documents and filse
    documents = Document.query.filter_by(person_id=id)
    for document in documents:
        # delete photo and thumbnail
        if document.type == "photo":
            subfolder = "thumbnail/"
            delete_file(document.name, "thumbnail/")
            delete_file(document.name, "photo/")
        else:
            delete_file(document.name)

    Document.query.filter_by(person_id=id).delete()

    # Delete skills
    Skill.query.filter_by(person_id=id).delete()

    # Delete profile picture
    if person.profile_image:
        delete_file(person.profile_image, "profile/")

    # Delete cv
    if person.cv:
        delete_file(person.cv)

    # Delete person
    db.session.delete(person)
    db.session.commit()

    flash('Profile for %s %s deleted.' % (person.name, person.surname), 'info')

    return redirect(url_for('catalog.profiles'))

@catalog.route('/photo-delete')
def photo_delete():
    if 'username' not in session:
        return redirect(url_for('catalog.login'))

    photo_id = request.args.get('photo_id')
    photo = Document.query.get_or_404(photo_id)
    if photo.type == "photo":
        delete_file(photo.name, "thumbnail/")
        delete_file(photo.name, "photo/")
    else:
        delete_file(photo.name)
    db.session.delete(photo)
    db.session.commit()

    return Response(json.dumps({'message': 'success'}), status=200, mimetype='application/json')

@catalog.route('/photo-rotate')
def photo_rotate():
    if 'username' not in session:
        return redirect(url_for('catalog.login'))

    photo_id = request.args.get('photo_id')
    angle = request.args.get('angle', -90) # default: clockwise
    angle = float(angle)
    photo = Document.query.get_or_404(photo_id)
    if photo.type != "photo":
        return

    im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'] + "photo/", photo.name))
    im = im.rotate(angle, 0, True)
    im.save(os.path.join(app.config['UPLOAD_FOLDER'] + "photo/", photo.name), "JPEG")
    # refresh thumbnails
    photo_resize(os.path.join(app.config['UPLOAD_FOLDER'] + "photo/", photo.name), photo.name, 250, 375, False, "thumbnail/")

    return Response(json.dumps({'message': 'success'}), status=200, mimetype='application/json')

@catalog.route('/profile-photo-rotate')
def profile_photo_rotate():
    if 'username' not in session:
        return redirect(url_for('catalog.login'))

    person_id = request.args.get('person_id')
    angle = request.args.get('angle', -90) # default: clockwise
    angle = float(angle)

    profile = Person.query.get_or_404(person_id)

    im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'] + "profile/", profile.profile_image))
    im = im.rotate(angle, 0, True)
    im.save(os.path.join(app.config['UPLOAD_FOLDER'] + "profile/", profile.profile_image), "JPEG")

    return redirect(url_for('catalog.update_profile', id=person_id))

@catalog.route('/batch-photo-delete')
def batch_photo_delete():
    if 'username' not in session:
        return redirect(url_for('catalog.login'))

    person_id = request.args.get('person_id')
    Person.query.get_or_404(person_id)

    photo_ids = request.args.getlist('photos[]')
    photos = Document.query \
        .filter(Document.id.in_(photo_ids)) \
        .all()

    for photo in photos:
        if photo.type == "photo":
            delete_file(photo.name, "thumbnail/")
            delete_file(photo.name, "photo/")
        else:
            delete_file(photo.name)
        db.session.delete(photo)
    db.session.commit()

    return Response(json.dumps({'message': 'success'}), status=200, mimetype='application/json')

@catalog.route('/batch-photo-rotate')
def batch_photo_rotate():
    if 'username' not in session:
        return redirect(url_for('catalog.login'))

    person_id = request.args.get('person_id')
    Person.query.get_or_404(person_id)

    photo_ids = request.args.getlist('photos[]')
    angle = request.args.get('angle', -90) # default: clockwise
    angle = float(angle)
    photos = Document.query \
        .filter(Document.id.in_(photo_ids)) \
        .all()

    for photo in photos:
        if photo.type != "photo":
            return

        im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'] + "photo/", photo.name))
        im = im.rotate(angle, 0, True)
        im.save(os.path.join(app.config['UPLOAD_FOLDER'] + "photo/", photo.name), "JPEG")
        # refresh thumbnails
        photo_resize(os.path.join(app.config['UPLOAD_FOLDER'] + "photo/", photo.name), photo.name, 250, 375, False, "thumbnail/")

    return Response(json.dumps({'message': 'success'}), status=200, mimetype='application/json')



@catalog.route('/batch-update-profile-photo', methods=['GET'])
def batch_update_profile_photo():
    person_id = request.args.get('person_id')
    Person.query.get_or_404(person_id)
    date_param = request.args.get('date')

    photo_ids = request.args.getlist('photos[]')
    photos = Document.query \
        .filter(Document.id.in_(photo_ids)) \
        .all()

    for photo in photos:
        if date_param == '':
            return Response(json.dumps({'message': 'Invalid date format'}), status=400, mimetype='application/json')

        photo.created = datetime.datetime.strptime(date_param, '%d-%m-%Y %H:%M:%S')
        db.session.add(photo)
    db.session.commit()

    return Response(json.dumps({'message': 'success'}), status=200, mimetype='application/json')

@catalog.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        if (app.config['USER'] != '' and app.config['PIN'] != '' and (app.config['USER'] == username) and (app.config['PIN'] == password) ):
            session['username'] = username
            return redirect(url_for('catalog.create_enter'))

    return render_template('login.html', form=form)

@catalog.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('catalog.login'))

manager.create_api(Classifier, methods=['GET'], results_per_page=None, exclude_columns=['skills'])

admin.add_view(ModelView(Classifier, db.session))

