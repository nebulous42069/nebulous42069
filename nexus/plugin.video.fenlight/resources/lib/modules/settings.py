# -*- coding: utf-8 -*-
from caches.settings_cache import get_setting, set_setting
from modules import kodi_utils
# logger = kodi_utils.logger

translate_path, get_property, tmdb_default_api = kodi_utils.translate_path, kodi_utils.get_property, kodi_utils.tmdb_default_api
download_directories_dict = {'movie': 'fenlight.movie_download_directory', 'episode': 'fenlight.tvshow_download_directory', 'thumb_url': 'fenlight.image_download_directory',
							'image_url': 'fenlight.image_download_directory','image': 'fenlight.image_download_directory', 'premium': 'fenlight.premium_download_directory',
							None: 'fenlight.premium_download_directory', 'None': False}
results_window_numbers_dict = {'List': 2000, 'Rows': 2001, 'WideList': 2002}
default_action_dict = {'0': 'play', '1': 'cancel', '2': 'pause'}
extras_open_action_dict = {'movie': (1, 3), 'tvshow': (2, 3)}
paginate_dict = {True: 'fenlight.paginate.limit_widgets', False: 'fenlight.paginate.limit_addon'}
prescrape_scrapers_tuple = ('easynews', 'rd_cloud', 'pm_cloud', 'ad_cloud', 'folders')
sort_to_top_dict = {'folders': 'fenlight.results.sort_folders_first', 'rd_cloud': 'fenlight.results.sort_rdcloud_first',
					'pm_cloud': 'fenlight.results.sort_pmcloud_first', 'ad_cloud': 'fenlight.results.sort_adcloud_first'}
internal_scrapers_clouds_list = [('rd', 'provider.rd_cloud'), ('pm', 'provider.pm_cloud'), ('ad', 'provider.ad_cloud')]

def results_format():
	window_format = str(get_setting('fenlight.results.list_format', 'List'))
	if not window_format in results_window_numbers_dict:
		window_format = 'List'
		set_setting('results.list_format', window_format)
	window_number = results_window_numbers_dict[window_format]
	return window_format.lower(), window_number

def store_resolved_to_cloud(debrid_service, pack):
	setting_value = int(get_setting('fenlight.store_resolved_to_cloud.%s' % debrid_service.lower(), '0'))
	return setting_value in (1, 2) if pack else setting_value == 1

def enabled_debrids_check(debrid_service):
	if not get_setting('fenlight.%s.enabled' % debrid_service) == 'true': return False
	return authorized_debrid_check(debrid_service)

def authorized_debrid_check(debrid_service):
	if get_setting('fenlight.%s.token' % debrid_service) in (None, '', 'empty_setting'): return False
	return True

def playback_settings():
	return (int(get_setting('fenlight.playback.watched_percent', '90')), int(get_setting('fenlight.playback.resume_percent', '5')))

def limit_resolve():
	return get_setting('fenlight.playback.limit_resolve', 'false') == 'true'

def movies_directory():
	return translate_path(get_setting('fenlight.movies_directory'))
	
def tv_show_directory():
	return translate_path(get_setting('fenlight.tv_shows_directory'))

def download_directory(media_type):
	return translate_path(get_setting(download_directories_dict[media_type]))

def auto_start_fenlight():
	return get_setting('fenlight.auto_start_fenlight', 'false') == 'true'

def source_folders_directory(media_type, source):
	setting = 'fenlight.%s.movies_directory' % source if media_type == 'movie' else 'fenlight.%s.tv_shows_directory' % source
	if get_setting(setting) not in ('', 'None', None): return translate_path( get_setting(setting))
	else: return False

def paginate(is_home):
	paginate_lists = int(get_setting('fenlight.paginate.lists', '0'))
	if is_home: return paginate_lists in (2, 3)
	else: return paginate_lists in (1, 3)

def page_limit(is_home):	
	return int(get_setting(paginate_dict[is_home], '20'))

def quality_filter(setting):
	return get_setting('fenlight.%s' % setting).split(', ')

def audio_filters():
	setting = get_setting('fenlight.filter_audio')
	if setting in ('empty_setting', ''): return []
	return setting.split(', ')

def include_prerelease_results():
	return get_setting('fenlight.include_prerelease_results', 'true') == 'true'

def auto_play(media_type):
	return get_setting('fenlight.auto_play_%s' % media_type, 'false') == 'true'

def autoplay_next_episode():
	if auto_play('episode') and get_setting('fenlight.autoplay_next_episode', 'false') == 'true': return True
	else: return False

def autoscrape_next_episode():
	if not auto_play('episode') and get_setting('fenlight.autoscrape_next_episode', 'false') == 'true': return True
	else: return False

def auto_rescrape_with_all():
	return int(get_setting('fenlight.results.auto_rescrape_with_all', '0'))

def auto_nextep_settings(play_type):
	play_type = 'autoplay' if play_type == 'autoplay_nextep' else 'autoscrape'
	window_percentage = 100 - int(get_setting('fenlight.%s_next_window_percentage' % play_type, '95'))
	use_chapters = get_setting('fenlight.%s_use_chapters' % play_type, 'true') == 'true'
	scraper_time = int(get_setting('fenlight.results.timeout', '60')) + 20
	default_action = default_action_dict[get_setting('fenlight.autoplay_default_action', '1')] if play_type == 'autoplay' else ''
	return {'scraper_time': scraper_time, 'window_percentage': window_percentage, 'default_action': default_action, 'use_chapters': use_chapters}

def filter_status(filter_type):
	return int(get_setting('fenlight.filter_%s' % filter_type, '0'))

def ignore_results_filter():
	return int(get_setting('fenlight.results.ignore_filter', '0'))

def trakt_sync_interval():
	setting = get_setting('fenlight.trakt.sync_interval', '25')
	interval = int(setting) * 60
	return setting, interval

def lists_sort_order(setting):
	return int(get_setting('fenlight.sort.%s' % setting, '0'))

def auto_start():
	return get_setting('fenlight.auto_start', 'false') == 'true'

def use_minimal_media_info():
	return get_setting('fenlight.use_minimal_media_info', 'true') == 'true'

def single_ep_display_format(is_external):
	if is_external: setting, default = 'fenlight.single_ep_display_widget', '1'
	else: setting, default = 'fenlight.single_ep_display', ''
	return int(get_setting(setting, default))

def easynews_active():
	if get_setting('fenlight.provider.easynews', 'false') == 'true': easynews_status = easynews_authorized()
	else: easynews_status = False
	return easynews_status

def easynews_authorized():
	easynews_user = get_setting('fenlight.easynews_user', 'empty_setting')
	easynews_password = get_setting('fenlight.easynews_password', 'empty_setting')
	if easynews_user in ('empty_setting', '') or easynews_password in ('empty_setting', ''): easynews_status = False
	else: easynews_status = True
	return easynews_status

def extras_enable_extra_ratings():
	return get_setting('fenlight.extras.enable_extra_ratings', 'true') == 'true'

def extras_enable_scrollbars():
	return get_setting('fenlight.extras.enable_scrollbars', 'true')

def extras_enabled_menus():
	setting = get_setting('fenlight.extras.enabled', '2000,2050,2051,2052,2053,2054,2055,2056,2057,2058,2059,2060,2061')
	if setting in ('', None, 'noop', []): return []
	return [int(i) for i in setting.split(',')]

def check_prescrape_sources(scraper, media_type):
	if scraper in prescrape_scrapers_tuple: return get_setting('fenlight.check.%s' % scraper) == 'true'
	if get_setting('fenlight.check.%s' % scraper) == 'true' and auto_play(media_type): return True
	else: return False

def external_scraper_info():
	module = get_setting('fenlight.external_scraper.module')
	if module in ('empty_setting', ''): return None, ''
	return module, module.split('.')[-1]

def filter_by_name(scraper):
	if get_property('fs_filterless_search') == 'true': return False
	return get_setting('fenlight.%s.title_filter' % scraper, 'false') == 'true'

def easynews_language_filter():
	enabled = get_setting('fenlight.easynews.filter_lang') == 'true'
	if enabled: filters = get_setting('fenlight.easynews.lang_filters').split(', ')
	else: filters = []
	return enabled, filters

def results_sort_order():
	return (
			lambda k: (k['quality_rank'], k['provider_rank'], -k['size']), #Quality, Provider, Size
			lambda k: (k['quality_rank'], -k['size'], k['provider_rank']), #Quality, Size, Provider
			lambda k: (k['provider_rank'], k['quality_rank'], -k['size']), #Provider, Quality, Size
			lambda k: (k['provider_rank'], -k['size'], k['quality_rank']), #Provider, Size, Quality
			lambda k: (-k['size'], k['quality_rank'], k['provider_rank']), #Size, Quality, Provider
			lambda k: (-k['size'], k['provider_rank'], k['quality_rank'])  #Size, Provider, Quality
			)[int(get_setting('fenlight.results.sort_order', '1'))]

def active_internal_scrapers():
	settings = ['provider.external', 'provider.easynews', 'provider.folders']
	settings_append = settings.append
	for item in internal_scrapers_clouds_list:
		if enabled_debrids_check(item[0]): settings_append(item[1])
	active = [i.split('.')[1] for i in settings if get_setting('fenlight.%s' % i) == 'true']
	return active

def provider_sort_ranks():
	en_priority = int(get_setting('fenlight.en.priority', '7'))
	rd_priority = int(get_setting('fenlight.rd.priority', '8'))
	ad_priority = int(get_setting('fenlight.ad.priority', '9'))
	pm_priority = int(get_setting('fenlight.pm.priority', '10'))
	return {'easynews': en_priority, 'real-debrid': rd_priority, 'premiumize.me': pm_priority, 'alldebrid': ad_priority,
			'rd_cloud': rd_priority, 'pm_cloud': pm_priority, 'ad_cloud': ad_priority, 'folders': 0}

def sort_to_top(provider):
	return get_setting(sort_to_top_dict[provider]) == 'true'

def auto_resume(media_type):
	auto_resume = get_setting('fenlight.auto_resume_%s' % media_type)
	if auto_resume == '1': return True
	if auto_resume == '2' and auto_play(media_type): return True
	else: return False

def scraping_settings():
	highlight_type = int(get_setting('fenlight.highlight.type', '0'))
	if highlight_type == 2:
		highlight = get_setting('fenlight.scraper_single_highlight', 'FF008EB2')
		return {'highlight_type': 1, '4k': highlight, '1080p': highlight, '720p': highlight, 'sd': highlight}
	easynews_highlight, debrid_cloud_highlight, folders_highlight = '', '', ''
	rd_highlight, pm_highlight, ad_highlight, highlight_4K, highlight_1080P, highlight_720P, highlight_SD = '', '', '', '', '', '', ''
	if highlight_type == 0:
		easynews_highlight = get_setting('fenlight.provider.easynews_highlight', 'FF00B3B2')
		debrid_cloud_highlight = get_setting('fenlight.provider.debrid_cloud_highlight', 'FF7A01CC')
		folders_highlight = get_setting('fenlight.provider.folders_highlight', 'FFB36B00')
		rd_highlight = get_setting('fenlight.provider.rd_highlight', 'FF3C9900')
		pm_highlight = get_setting('fenlight.provider.pm_highlight', 'FFFF3300')
		ad_highlight = get_setting('fenlight.provider.ad_highlight', 'FFE6B800')
	else:
		highlight_4K = get_setting('fenlight.scraper_4k_highlight', 'FFFF00FE')
		highlight_1080P = get_setting('fenlight.scraper_1080p_highlight', 'FFE6B800')
		highlight_720P = get_setting('fenlight.scraper_720p_highlight', 'FF3C9900')
		highlight_SD = get_setting('fenlight.scraper_SD_highlight', 'FF0166FF')
	return {'highlight_type': highlight_type,'real-debrid': rd_highlight, 'premiumize': pm_highlight, 'alldebrid': ad_highlight, 'rd_cloud': debrid_cloud_highlight,
			'pm_cloud': debrid_cloud_highlight, 'ad_cloud': debrid_cloud_highlight, 'easynews': easynews_highlight, 'folders': folders_highlight,
			'4k': highlight_4K, '1080p': highlight_1080P, '720p': highlight_720P, 'sd': highlight_SD}

def omdb_api_key():
	return get_setting('fenlight.omdb_api', 'empty_setting')

def default_all_episodes():
	return int(get_setting('fenlight.default_all_episodes', '0'))

def widget_hide_next_page():
	return get_setting('fenlight.widget_hide_next_page', 'false') == 'true'

def widget_hide_watched():
	return get_setting('fenlight.widget_hide_watched', 'false') == 'true'

def calendar_sort_order():
	return int(get_setting('fenlight.trakt.calendar_sort_order', '0'))

def date_offset():
	return int(get_setting('fenlight.datetime.offset', '0')) + 5

def extras_open_action(media_type):
	return int(get_setting('fenlight.extras.open_action', '0')) in extras_open_action_dict[media_type]

def watched_indicators():
	if get_setting('fenlight.trakt.user') in ('empty_setting', ''): return 0
	return int(get_setting('fenlight.watched_indicators', '0'))

def nextep_include_unwatched():
	return int(get_setting('fenlight.nextep.include_unwatched', '0'))

def nextep_include_unaired():
	return get_setting('fenlight.nextep.include_unaired', 'false') == 'true'

def update_delay():
	return int(get_setting('fenlight.update.delay', '45'))

def update_action():
	return int(get_setting('fenlight.update.action', '2'))

def update_use_test_repo():
	return get_setting('fenlight.update.use_test_repo', 'true') == 'true'
