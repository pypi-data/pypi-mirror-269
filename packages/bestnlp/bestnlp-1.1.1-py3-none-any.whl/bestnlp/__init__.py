from bestnlp.new_word_discovery import NewWordDiscovery
nwd = NewWordDiscovery()
new_words = nwd.extract_keyword

from bestnlp.similar_word_discovery import SimilarWordDiscovery
swd = SimilarWordDiscovery()
similar_words = swd.find_similar
get_search_similar = swd.get_search_similar
get_click_similar = swd.get_click_similar