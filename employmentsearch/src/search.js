import React from "react";

import {
    Hits,
    Layout,
    SearchBox,
    RefinementListFilter,
    HierarchicalMenuFilter,
    ItemList,
    Panel,
    Pagination,
    HitsStats,
    ResetFilters,
    SearchkitProvider,
    SearchkitManager,
    SelectedFilters,
    SortingSelector
} from "searchkit"

const searchkit = new SearchkitManager("services/");

searchkit.addResultsListener((results)=>{
    console.log(results);
})

searchkit.translateFunction = (key) => {
    let translations = {
        "pagination.previous": "Edelliset",
        "pagination.next": "Seuraavat",
        "hitstats.results_found": "{hitCount} hakutulosta"
    };
    return translations[key]
};

const HitItem = (props) => {
    var tags = [];
    tags.push(...props.result._source.classification);

    let result =
        <div className="hit-item">
            <a className="hit-item-title"
               href={"details/" + props.result._source.id}>{props.result._source.name}</a><br/>
            {props.result._source.organization}<br/>
            {/*<small>{tags.join(' // ')}</small>
            <br/>*/}
            {props.result._source.ingress}
        </div>;
    return result
};

const SelectedFilter = (props) => (
    <div className={props.bemBlocks.option()
        .mix(props.bemBlocks.container("item"))
        .mix(`selected-filter--${props.filterId}`)()}>
        <div className={props.bemBlocks.option("name")}>{props.labelValue}</div>
        <div className={props.bemBlocks.option("remove-action")} onClick={props.removeFilter}>x</div>
    </div>
);

class Search extends React.Component {
    render() {
        let hidden = {visibility: 'hidden'};
        let middle = {display: 'flex', justifyContent: 'center'};
        let margintop = {marginTop: 15};

        const openHelp = () => {
            window.show_info();
//            window.location.href = "/info";
        };

        return (
            <SearchkitProvider searchkit={searchkit}>
                <Layout>
                    <div className="flexbox">

                        <div className="left">
                            <div className="column-title" style={middle}>Valinnat</div>
                          <SearchBox
                            placeholder="Haku"
                            searchOnChange={true}
                            queryOptions={{analyzer:"stop"}}
                            queryFields={["name^5", "ingress^3", "description", "description2", "description3", "description4"]}
                          />
                            <div className="target-choices">
                                <Panel collapsable={true} defaultCollapsed={true} title="Neuvonta- ja ohjauspalvelut">
                                    <HierarchicalMenuFilter id="target" fields={["target.raw"]} operator="OR"
                                                          listComponent={ItemList} orderKey="_term"/>
                                </Panel>
                            </div>
                            <div className="target-service_path">
                                <Panel collapsable={true} defaultCollapsed={true} title="Koulutuspalvelut">
                                    <RefinementListFilter id="service_path" field="service_path.raw" operator="OR"
                                                          listComponent={ItemList} orderKey="_term"/>
                                </Panel>
                            </div>
                            <div style={margintop}>
                                    <Panel collapsable={true} defaultCollapsed={true} title="Työllistymisedellytyksiä lisäävät palvelut">
                                        <RefinementListFilter id="classification" field="classification.raw"
                                                              operator="OR" listComponent={ItemList} orderKey="_term"/>
                                    </Panel>
                            </div>


                            <Panel collapsable={true} defaultCollapsed={true} title="Työnhaku- ja työnvälityspalvelut">
                                <RefinementListFilter id="immigration" field="immigration.raw"
                                    operator="OR" listComponent={ItemList} orderKey="_term"/>
                            </Panel>
                            <Panel collapsable={true} defaultCollapsed={true} title="Yrittäjyyspalvelut">
                                <RefinementListFilter id="age_group" field="age_group.raw"
                                    operator="OR" listComponent={ItemList} orderKey="_term"/>
                            </Panel>
                            <Panel collapsable={true} defaultCollapsed={true} title=" Terveys-, kuntoutus- ja sosiaalipalvelut">
                                <RefinementListFilter id="unemployment_duration" field="unemployment_duration.raw"
                                    operator="OR" listComponent={ItemList} orderKey="_term"/>
                            </Panel>
                            <Panel collapsable={true} defaultCollapsed={true} title="Muut palvelut">
                                <RefinementListFilter id="health" field="health.raw"
                                    operator="OR" listComponent={ItemList} orderKey="_term"/>
                            </Panel>
                            <Panel collapsable={true} defaultCollapsed={true} title="Palveluja kohderyhmittäin">
                                <RefinementListFilter id="integration" field="integration.raw"
                                    operator="OR" listComponent={ItemList} orderKey="_term"/>
                            </Panel>

                            <br/>
                        </div>

                        <div className="right">
                            <div className="column-title" style={middle}>Palvelut</div>
                            <ResetFilters translations={{"reset.clear_all": "Poista hakusuodattimet"}}/>
                            {/*<SelectedFilters itemComponent={SelectedFilter}/>*/}
                            <HitsStats/>
                            <Pagination showNumbers={true}/>
                            <div className="results">
                                <Hits hitsPerPage={100} itemComponent={HitItem}/>
                            </div>
                            <Pagination showNumbers={true}/>
                            <div style={hidden}>
                                <SortingSelector options={[
                                    {
                                        label: "Lajiteltu", key: "sorting", fields: [
                                        {field: "search_result_priority", options: {order: "asc"}},
                                        {field: "name.keyword", options: {order: "asc"}}
                                    ]
                                    }]}/>
                            </div>
                        </div>

                    </div>
                </Layout>
            </SearchkitProvider>
        );
    }
};

export default Search;