# import pandas as pd
import bestnlp.utils as utils
import math


class SimilarWordDiscovery():
    """
    search dataframe
    time  keyword  user_id

    click dataframe
    time  keyword  user_id  item_id
    """
    def process_search(self, search_df, threshold, time_name="time", user_id_name="user_id", keyword_name="keyword"):
        #搜索行为
        df = search_df.sort_values(time_name)
        df = df.groupby(user_id_name)[keyword_name].agg(list).reset_index()
        # di = dict()
        # for keyword in df[keyword_name].tolist():
        #     if len(keyword) >= 2:
        #         for i in range(len(keyword) - 1):
        #             if keyword[i] == keyword[i + 1]: continue
        #             key = frozenset([keyword[i], keyword[i + 1]])
        #             di[key] = di.get(key, 0) + 1
        # res = dict()
        # for key, value in di.items():
        #     if value >= threshold:
        #         res[key] = value
        # return res
        di = dict()
        for keyword in df[keyword_name].tolist():
            if len(keyword) >= 2:
                for i in range(len(keyword) - 1):
                    if keyword[i] == keyword[i + 1]: continue
                    if keyword[i] not in di:
                        di[keyword[i]] = dict()
                    di[keyword[i]][keyword[i + 1]] = di[keyword[i]].get(keyword[i + 1], 0) + 1
        res = dict()
        for key, value in di.items():
            sum_num = sum(value.values())
            res[key] = dict()
            for key2 in value:
                ratio = value[key2]/sum_num
                if value[key2] > threshold:
                    res[key][key2] = value[key2]
        for key, value in res.items():
            for key2 in value:
                print(key, key2, value[key2])
        final_res = dict()
        for key, value in res.items():
            for key2 in value:
                if key2 in res and key in res[key2]:
                    final_res[frozenset([key, key2])] = res[key][key2] + res[key2][key]
        return final_res


    def process_click(self, click_df, threshold, time_name="time", user_id_name="user_id", keyword_name="keyword", item_id_name="item_id"):
        #点击行为
        #同一个商品点击等行为对应的搜索词
        act_df = click_df.sort_values(time_name).drop_duplicates([user_id_name, keyword_name, item_id_name])
        df = act_df.groupby(item_id_name)[keyword_name].agg(list).reset_index()
        # di = dict()
        # for keyword in df[keyword_name].tolist():
        #     if len(keyword) >= 2:
        #         for key1 in keyword:
        #             for key2 in keyword:
        #                 if key1 == key2: continue
        #                 key = frozenset([key1, key2])
        #                 di[key] = di.get(key, 0) + 1
        # res = dict()
        # for key, value in di.items():
        #     if value >= threshold:
        #         res[key] = value
        # return res
        di = dict()
        for keyword in df[keyword_name].tolist():
            if len(keyword) >= 2:
                for i in range(len(keyword) - 1):
                    if keyword[i] == keyword[i + 1]: continue
                    if keyword[i] not in di:
                        di[keyword[i]] = dict()
                    di[keyword[i]][keyword[i + 1]] = di[keyword[i]].get(keyword[i + 1], 0) + 1
        res = dict()
        for key, value in di.items():
            sum_num = sum(value.values())
            res[key] = dict()
            for key2 in value:
                ratio = value[key2] / sum_num
                if value[key2] > threshold and ratio > 0.1:
                    res[key][key2] = value[key2]
        final_res = dict()
        for key, value in res.items():
            for key2 in value:
                if key2 in res and key in res[key2]:
                    final_res[frozenset([key, key2])] = res[key][key2] + res[key2][key]
        return final_res


    def find_similar(self, search_df, click_df, search_weight=1, click_weight=1, both=False, search_threshod=None, click_threshold=None, threshold=None, max_num=1000, time_name="time", user_id_name="user_id", keyword_name="keyword", item_id_name="item_id"):
        search_df = search_df[~((search_df[keyword_name].isnull()) | (search_df[keyword_name] == ""))]
        search_df[keyword_name] = search_df[keyword_name].apply(lambda x: x.strip().lower())
        if search_threshod is None:
            search_threshod = max([5, math.pow(len(set(search_df[keyword_name])), 1 / 4),
                             math.pow(len(search_df[keyword_name]) / 2, 1 / 4)])
            print("default search threshold: ", search_threshod)
        click_df = click_df[~((click_df[keyword_name].isnull()) | (click_df[keyword_name] == ""))]
        click_df[keyword_name] = click_df[keyword_name].apply(lambda x: x.strip().lower())
        if click_threshold is None:
            click_threshold = max(
                [10, math.pow(len(set(click_df[keyword_name])), 1 / 4), math.pow(len(click_df[keyword_name]) / 2, 1 / 4)])
            print("default click threshold: ", click_threshold)

        search_res = self.process_search(search_df, search_threshod, time_name=time_name, user_id_name=user_id_name, keyword_name=keyword_name) if search_df is not None else dict()
        click_res = self.process_click(click_df, click_threshold, time_name=time_name, user_id_name=user_id_name, keyword_name=keyword_name, item_id_name=item_id_name) if click_df is not None else dict()
        if threshold is None:
            threshold = search_threshod * search_weight + click_threshold * click_weight
            print("default threshold: ", threshold)
        res = dict()
        if both:
            keys = set(search_res.keys()).intersection(set(click_res.keys()))
        else:
            keys = set(search_res.keys()).union(set(click_res.keys()))
        for key in keys:
            score = search_res.get(key, 0) * search_weight + click_res.get(key, 0) * click_weight
            if score >= threshold:
                res[key] = score
        res = list(sorted(res.items(), key=lambda x: x[1], reverse=True))
        res = res[:max_num if len(res) > max_num else len(res)]
        return res


    def get_search_similar(self, search_df, threshold=None, time_name="time", user_id_name="user_id", keyword_name="keyword"):
        #搜索行为
        search_df[keyword_name] = search_df[keyword_name].apply(lambda x: x.strip().lower())
        search_df = search_df[~((search_df[keyword_name].isnull()) | (search_df[keyword_name]==""))]
        if threshold is None:
            threshold = 5
        print("default search threshold: ", threshold)
        df = search_df.sort_values(time_name)
        df = df.groupby(user_id_name)[keyword_name].agg(list).reset_index()
        di = dict()
        for keyword in df[keyword_name].tolist():
            if len(keyword) >= 2:
                for i in range(len(keyword) - 1):
                    if keyword[i] == keyword[i + 1]: continue
                    if keyword[i] not in di:
                        di[keyword[i]] = dict()
                    di[keyword[i]][keyword[i + 1]] = di[keyword[i]].get(keyword[i + 1], 0) + 1
        res = dict()
        for key, value in di.items():
            sum_num = sum(value.values())
            res[key] = dict()
            for key2 in value:
                ratio = value[key2]/sum_num
                if value[key2] > 10:
                    res[key][key2] = (value[key2], ratio)
        return res


    def get_click_similar(self, click_df, threshold=None, time_name="time", user_id_name="user_id", keyword_name="keyword", item_id_name="item_id"):
        #点击行为
        #同一个商品点击等行为对应的搜索词
        click_df[keyword_name] = click_df[keyword_name].apply(lambda x: x.strip().lower())
        click_df = click_df[~((click_df[keyword_name].isnull()) | (click_df[keyword_name]==""))]
        if threshold is None:
            threshold = 5
        print("default click threshold: ", threshold)
        act_df = click_df.sort_values(time_name).drop_duplicates([user_id_name, keyword_name, item_id_name])
        df = act_df.groupby(item_id_name)[keyword_name].agg(list).reset_index()
        di = dict()
        for keyword in df[keyword_name].tolist():
            if len(keyword) >= 2:
                for i in range(len(keyword) - 1):
                    if keyword[i] == keyword[i + 1]: continue
                    if keyword[i] not in di:
                        di[keyword[i]] = dict()
                    di[keyword[i]][keyword[i + 1]] = di[keyword[i]].get(keyword[i + 1], 0) + 1
        res = dict()
        for key, value in di.items():
            sum_num = sum(value.values())
            res[key] = dict()
            for key2 in value:
                ratio = value[key2] / sum_num
                if value[key2] > threshold:
                    res[key][key2] = (value[key2], ratio)
        return res


# import pandas as pd
# df = pd.read_excel("df_details.xlsx")
# search_df = df[df["action_type"]=="search"][["timestamp", "query", "userid"]]
# search_df.rename(columns={"timestamp":"time", "query":"keyword", "userid":"user_id"}, inplace=True)
# click_df = df[df["action_type"]=="click"][["timestamp", "query", "userid", "itemid"]]
# click_df.rename(columns={"timestamp":"time", "query":"keyword", "userid":"user_id", "itemid":"item_id"}, inplace=True)
# swd = SimilarWordDiscovery()
# res = swd.find_similar(search_df, click_df)
# print(res)
# print(len(res))
# for elem in res:
#     print(elem)
# res = swd.get_search_similar(search_df)
# for key1 in res:
#     for key2 in res[key1]:
#         if res[key1][key2][0] > 10 and res[key1][key2][1] > 0.35 and (key2 not in res or key1 not in res[key2] or res[key2][key1][1] < 0.1 or res[key2][key1][0] < 5):
#             print(key1, key2, res[key1][key2][0], res[key1][key2][1], res.get(key2, dict()).get(key1, [0, 0])[0], res.get(key2, dict()).get(key1, [0, 0])[1])




# import pandas as pd
# search_df = pd.read_excel("search.xlsx")
# click_df = pd.read_excel("click.xlsx")
# print(search_df)
# print(click_df)
#
# search_df.rename(columns={"search_term":"keyword", "distinct_id":"user_id"}, inplace=True)
# click_df["keyword"] = click_df["url"].apply(lambda x: str(x)[6:])
# click_df.rename(columns={"distinct_id":"user_id", "article_number":"item_id"}, inplace=True)

# swd = SimilarWordDiscovery()
# res = swd.find_similar(search_df, click_df)
# print(res)
# print(len(res))
# for elem in res:
#     print(elem)
# res = swd.get_search_similar(search_df)
# for key1 in res:
#     for key2 in res[key1]:
#         if res[key1][key2][0] > 10 and res[key1][key2][1] > 0.35 and (key2 not in res or key1 not in res[key2] or res[key2][key1][1] < 0.1 or res[key2][key1][0] < 5):
#             print(key1, key2, res[key1][key2][0], res[key1][key2][1], res.get(key2, dict()).get(key1, [0, 0])[0], res.get(key2, dict()).get(key1, [0, 0])[1])







